"""The WebSocket connection to an appliance, in either of its two encryption schemes.

Appliances use one of two schemes (see hcpy, MIT, THIRD_PARTY_NOTICES.md):

- **TLS-PSK:** `wss://<host>:443/homeconnect`, TLS 1.2 with a pre-shared key and the identity
  `HCCOM_Local_App`. Needs Python 3.13's native TLS-PSK support.
- **AES:** `ws://<host>:80/homeconnect`, a plain WebSocket whose binary frames are encrypted
  and authenticated by `AesCodec`. Used when the profile contains an IV.

Either way the payload is JSON text; this module only moves text in and out.
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import socket
import ssl
from typing import TYPE_CHECKING, Literal

import aiohttp
from yarl import URL

from .crypto import AesCodec, decode_key
from .errors import (
    AuthenticationError,
    ConnectionClosedError,
    ConnectionFailedError,
    HomeDisconnectError,
)

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Self

_LOGGER = logging.getLogger(__name__)

# Identifiers in /ci/info and /iz/info that shouldn't end up in a log someone posts publicly,
# the same ones Home Connect Local's diagnostics leave out
_LOG_REDACT = frozenset({"deviceID", "mac", "serialNumber", "shipSki"})

PSK_IDENTITY = "HCCOM_Local_App"
WEBSOCKET_PATH = "/homeconnect"
TLS_PORT = 443
AES_PORT = 80


def _reason(err: BaseException) -> str:
    """Say in a few words why a connect failed.

    aiohttp's own text carries the SSL context's repr and the resolved address, which is noise
    in a message shown to a user. The original error stays attached as the cause.
    """
    if isinstance(err, TimeoutError):
        return "timed out"
    if isinstance(err, aiohttp.WSServerHandshakeError):
        return f"the WebSocket upgrade was answered with HTTP {err.status}"
    cause = getattr(err, "os_error", None) or err
    if isinstance(cause, socket.gaierror):
        return "the host name couldn't be resolved"
    if isinstance(cause, OSError) and cause.errno is not None:
        return os.strerror(cause.errno).lower()
    return "the connection failed"


def _redact(data: object) -> object:
    """Replace the values of identifier keys, at any depth."""
    if isinstance(data, dict):
        return {
            key: "**REDACTED**" if key in _LOG_REDACT else _redact(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_redact(item) for item in data]
    return data


def appliance_hostname(
    connection_type: Literal["AES", "TLS"], ha_id: str, brand: str, appliance_type: str
) -> str:
    """Return the host name an appliance announces over mDNS, without `.local`.

    TLS appliances use `{brand}-{type}-{haId}`, AES appliances their `haId` alone. Whether it
    resolves is up to the network: the operating system needs mDNS support, or a router that
    puts DHCP host names in its DNS. Resolving it through an mDNS library, or using the address
    from the appliance's announcement, is more reliable.
    """
    if connection_type == "TLS":
        return f"{brand}-{appliance_type}-{ha_id}"
    return ha_id


def create_psk_ssl_context(psk: bytes) -> ssl.SSLContext:
    """Create the TLS 1.2 PSK client context the appliances expect."""
    if not ssl.HAS_PSK:
        msg = "This Python's ssl module has no TLS-PSK support"
        raise HomeDisconnectError(msg)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # The appliance authenticates with the PSK; it has no certificate to check.
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    # The appliances don't support TLS 1.3 PSK.
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.set_ciphers("PSK")
    context.set_psk_client_callback(lambda _hint: (PSK_IDENTITY, psk))
    return context


class Transport:
    """One WebSocket connection to one appliance.

    The caller owns the `aiohttp.ClientSession` (Home Assistant passes its shared session);
    closing the transport never closes the session.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        host: str,
        psk64: str,
        iv64: str | None = None,
        *,
        port: int | None = None,
        heartbeat: float | None = 20,
        name: str | None = None,
    ) -> None:
        """Pick the scheme from the profile: an IV means AES, no IV means TLS-PSK.

        `heartbeat` is the WebSocket ping interval in seconds; the connection closes when a
        ping goes unanswered. `None` turns it off.

        `name` (e.g. the model) goes in front of the host in the debug log, which shows every
        message sent and received.
        """
        self._session = session
        self._log_name = f"{name}/{host}" if name else host
        self._heartbeat = heartbeat
        psk = decode_key(psk64)
        self._codec: AesCodec | None
        self._ssl: ssl.SSLContext | bool
        if iv64:
            self._codec = AesCodec(psk, decode_key(iv64))
            self._ssl = False
            scheme, default_port = "ws", AES_PORT
        else:
            self._codec = None
            self._ssl = create_psk_ssl_context(psk)
            scheme, default_port = "wss", TLS_PORT
        self.url = URL.build(
            scheme=scheme, host=host, port=port or default_port, path=WEBSOCKET_PATH
        )
        self._websocket: aiohttp.ClientWebSocketResponse | None = None

    @property
    def encrypted_with_aes(self) -> bool:
        """Whether this connection uses the AES scheme rather than TLS-PSK."""
        return self._codec is not None

    @property
    def connected(self) -> bool:
        """Whether the WebSocket is open."""
        return self._websocket is not None and not self._websocket.closed

    @property
    def close_code(self) -> int | None:
        """The close code of the last connection, once it has closed."""
        return None if self._websocket is None else self._websocket.close_code

    async def connect(self) -> None:
        """Open the WebSocket. Every connection starts new encryption chains.

        There's no timeout of its own: wrap the call in `asyncio.timeout` to bound it.
        """
        if self.connected:
            return
        if self._codec is not None:
            self._codec.reset()
        try:
            self._websocket = await self._session.ws_connect(
                self.url, ssl=self._ssl, heartbeat=self._heartbeat
            )
        except (aiohttp.ClientError, OSError, TimeoutError) as err:
            if self._rejected_psk(err):
                msg = f"{self.url} rejected the key during the TLS handshake"
                raise AuthenticationError(msg) from err
            msg = f"Can't connect to {self.url}: {_reason(err)}"
            raise ConnectionFailedError(msg) from err

    def _log(self, direction: str, message: str) -> None:
        """Log a message at debug level, with the appliance's identifiers left out."""
        if not _LOGGER.isEnabledFor(logging.DEBUG):
            return
        # Logging must never break the connection, even for a message that isn't JSON
        with contextlib.suppress(ValueError):
            message = json.dumps(_redact(json.loads(message)))
        _LOGGER.debug("%s %s: %s", direction, self._log_name, message)

    def _rejected_psk(self, err: BaseException) -> bool:
        """Whether a TLS-PSK connect failed in the handshake, i.e. after TCP connected.

        A wrong PSK ends the TLS handshake with an SSL error or a reset. A refused
        connection, a timeout or an unreachable host is a network problem instead.
        """
        if self._codec is not None:
            return False
        if isinstance(err, (aiohttp.ClientSSLError, ssl.SSLError)):
            return True
        cause = getattr(err, "os_error", None) or err.__cause__
        return isinstance(cause, (ssl.SSLError, ConnectionResetError))

    async def send(self, message: str) -> None:
        """Send one JSON text message."""
        websocket = self._require_open()
        self._log("Sent to", message)
        try:
            if self._codec is not None:
                await websocket.send_bytes(self._codec.encrypt(message))
            else:
                await websocket.send_str(message)
        except (aiohttp.ClientError, ConnectionError) as err:
            raise ConnectionClosedError(websocket.close_code) from err

    async def receive(self) -> str:
        """Wait for the next message and return its JSON text.

        Raises `ConnectionClosedError` when the connection closes, and `DecryptionError` for an
        AES frame that fails authentication.
        """
        websocket = self._require_open()
        try:
            message = await websocket.receive()
        except (aiohttp.ClientError, ConnectionError, OSError) as err:
            # aiohttp answers the appliance's pings inside receive(); when the connection is
            # already half closed (e.g. after the machine slept and the appliance gave up on
            # us), that write raises instead of receive() returning a close message.
            with contextlib.suppress(aiohttp.ClientError, ConnectionError, OSError):
                await websocket.close()
            raise ConnectionClosedError(websocket.close_code) from err
        if message.type is aiohttp.WSMsgType.BINARY and self._codec is not None:
            text = self._codec.decrypt(message.data)
            self._log("Received from", text)
            return text
        if message.type is aiohttp.WSMsgType.TEXT and self._codec is None:
            text = str(message.data)
            self._log("Received from", text)
            return text
        if message.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSING,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.ERROR,
        ):
            raise ConnectionClosedError(websocket.close_code)
        msg = f"Unexpected {message.type.name} frame"
        raise HomeDisconnectError(msg)

    async def close(self) -> None:
        """Close the WebSocket if it's open."""
        if self._websocket is not None:
            await self._websocket.close()

    def _require_open(self) -> aiohttp.ClientWebSocketResponse:
        if self._websocket is None or self._websocket.closed:
            raise ConnectionClosedError(self.close_code)
        return self._websocket

    async def __aenter__(self) -> Self:
        """Connect when entering an `async with` block."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close when leaving an `async with` block."""
        await self.close()
