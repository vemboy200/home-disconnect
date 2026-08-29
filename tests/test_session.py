from __future__ import annotations

import asyncio
from copy import deepcopy
from typing import TYPE_CHECKING
from unittest.mock import ANY, AsyncMock, call

import pytest
from home_disconnect import (
    AllreadyConnectedError,
    AuthenticationError,
    ConnectionFailedError,
    ConnectionState,
    HCSession,
    HCSessionReconnect,
)
from home_disconnect.message import Action, Message
from home_disconnect.task_manager import TaskManager
from home_disconnect.testutils import TEST_APP_ID, TEST_APP_NAME

from const import (
    CLIENT_MESSAGE_ID,
    DEVICE_MESSAGE_SET_1,
    DEVICE_MESSAGE_SET_2,
    DEVICE_MESSAGE_SET_3,
    SERVER_MESSAGE_ID,
    SESSION_ID,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from tests.utils import ApplianceServerAes

    from utils import ApplianceServer


@pytest.mark.asyncio
async def test_session_connect_tls(
    appliance_server_tls: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connection."""
    appliance_server = await appliance_server_tls(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()
    message_handler = AsyncMock()

    session = HCSession(
        appliance_server.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=appliance_server.psk64,
        message_handler=message_handler,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED
    await session.connect()
    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await session.close()
    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )
    message_handler.assert_called_once_with(
        Message(
            sid=SESSION_ID,
            msg_id=SERVER_MESSAGE_ID,
            resource="/ei/initialValues",
            version=2,
            action=Action.POST,
            data=[{"edMsgID": CLIENT_MESSAGE_ID}],
            code=None,
        )
    )


@pytest.mark.asyncio
async def test_session_connect_aes(
    appliance_server_aes: Callable[..., Awaitable[ApplianceServerAes]],
) -> None:
    """Test Session connection failing."""
    appliance_server = await appliance_server_aes(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()
    message_handler = AsyncMock()

    session = HCSession(
        appliance_server.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=appliance_server.psk64,
        iv64=appliance_server.iv64,
        message_handler=message_handler,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED
    await session.connect()
    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await session.close()
    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )
    message_handler.assert_called_once_with(
        Message(
            sid=SESSION_ID,
            msg_id=SERVER_MESSAGE_ID,
            resource="/ei/initialValues",
            version=2,
            action=Action.POST,
            data=[{"edMsgID": CLIENT_MESSAGE_ID}],
            code=None,
        )
    )


@pytest.mark.asyncio
async def test_session_handshake_1(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session Handshake with Message set 1."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()
    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        connection_state_callback=connection_callback,
    )

    await session.connect()
    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )

    assert appliance.messages[0] == Message(
        sid=10,
        msg_id=20,
        resource="/ei/initialValues",
        version=2,
        action=Action.RESPONSE,
        data=[
            {
                "deviceType": "Application",
                "deviceName": "Test Device",
                "deviceID": "c6683b15",
            }
        ],
    )
    assert list(appliance.messages[0].data[0].items()) == list(
        {
            "deviceType": "Application",
            "deviceName": "Test Device",
            "deviceID": "c6683b15",
        }.items()
    )

    assert appliance.messages[1] == Message(
        sid=10, msg_id=30, resource="/ci/services", version=1, action=Action.GET
    )

    assert appliance.messages[2] == Message(
        sid=10, msg_id=31, resource="/iz/info", version=1, action=Action.GET
    )

    assert appliance.messages[3] == Message(
        sid=10, msg_id=32, resource="/ei/deviceReady", version=2, action=Action.NOTIFY
    )

    assert appliance.messages[4] == Message(
        sid=10, msg_id=33, resource="/ni/info", version=1, action=Action.GET
    )


@pytest.mark.asyncio
async def test_session_handshake_ni_info_error(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session Handshake completes even if /ni/info errors out."""
    message_set = deepcopy(DEVICE_MESSAGE_SET_1)
    del message_set["responses"]["/ni/info"]
    appliance = await appliance_server(message_set)
    connection_callback = AsyncMock()
    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        connection_state_callback=connection_callback,
    )

    await session.connect()
    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )


@pytest.mark.asyncio
async def test_session_handshake_2(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session Handshake with Message set 2."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_2)
    connection_callback = AsyncMock()

    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        connection_state_callback=connection_callback,
    )

    await session.connect()
    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )

    assert appliance.messages[0] == Message(
        sid=10,
        msg_id=20,
        resource="/ei/initialValues",
        version=1,
        action=Action.RESPONSE,
        data=[
            {
                "deviceType": 2,
                "deviceName": "Test Device",
                "deviceID": "c6683b15",
            }
        ],
    )
    assert list(appliance.messages[0].data[0].items()) == list(
        {
            "deviceType": 2,
            "deviceName": "Test Device",
            "deviceID": "c6683b15",
        }.items()
    )

    assert appliance.messages[1] == Message(
        sid=10, msg_id=30, resource="/ci/services", version=1, action=Action.GET
    )

    assert appliance.messages[2] == Message(
        sid=10,
        msg_id=31,
        resource="/ci/authentication",
        version=1,
        action=Action.GET,
        data=[{"nonce": ANY}],
    )

    assert appliance.messages[3] == Message(
        sid=10, msg_id=32, resource="/ci/info", version=1, action=Action.GET
    )


@pytest.mark.asyncio
async def test_session_handshake_3(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session Handshake with Message set 2."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_3)
    connection_callback = AsyncMock()

    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        connection_state_callback=connection_callback,
    )

    await session.connect()
    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )

    assert appliance.messages[0] == Message(
        sid=10,
        msg_id=20,
        resource="/ei/initialValues",
        version=2,
        action=Action.RESPONSE,
        data=[
            {
                "deviceType": "Application",
                "deviceName": "Test Device",
                "deviceID": "c6683b15",
            }
        ],
    )
    assert list(appliance.messages[0].data[0].items()) == list(
        {
            "deviceType": "Application",
            "deviceName": "Test Device",
            "deviceID": "c6683b15",
        }.items()
    )

    assert appliance.messages[1] == Message(
        sid=10, msg_id=30, resource="/ci/services", version=1, action=Action.GET
    )

    assert appliance.messages[2] == Message(
        sid=10,
        msg_id=31,
        resource="/ci/authentication",
        version=2,
        action=Action.GET,
        data=[{"nonce": ANY}],
    )

    assert appliance.messages[3] == Message(
        sid=10, msg_id=32, resource="/ci/info", version=2, action=Action.GET
    )

    assert appliance.messages[4] == Message(
        sid=10, msg_id=33, resource="/ei/deviceReady", version=2, action=Action.NOTIFY
    )

    assert appliance.messages[5] == Message(
        sid=10, msg_id=34, resource="/ni/info", version=1, action=Action.GET
    )


@pytest.mark.asyncio
async def test_session_connect_failed() -> None:
    """Test Session connction failing."""
    connection_callback = AsyncMock()

    session = HCSession(
        "127.0.0.1",
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        connection_state_callback=connection_callback,
    )

    with pytest.raises(ConnectionFailedError):
        await session.connect()

    assert not session.connected
    assert session.connection_state == ConnectionState.ABNORMAL_CLOSURE

    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.ABNORMAL_CLOSURE),
        ]
    )


@pytest.mark.asyncio
async def test_session_auth_error_tls(
    appliance_server_tls: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connction failing."""
    appliance_server = await appliance_server_tls(DEVICE_MESSAGE_SET_1)

    session = HCSession(
        appliance_server.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64="DucPCx_bN2d0fP07ptJDas_umP6YK63aAsrgl7kUWZk",
    )

    with pytest.raises(AuthenticationError):
        await session.connect()

    await session.close()


@pytest.mark.asyncio
async def test_session_auth_error_aes(
    appliance_server_aes: Callable[..., Awaitable[ApplianceServerAes]],
) -> None:
    """Test Session connction failing."""
    appliance_server = await appliance_server_aes(DEVICE_MESSAGE_SET_1)

    session = HCSession(
        appliance_server.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64="DucPCx_bN2d0fP07ptJDas_umP6YK63aAsrgl7kUWZk",
        iv64="8sJeiM2Hofw3XA7M1WB91E==",
    )

    with pytest.raises(AuthenticationError):
        await session.connect()

    await session.close()


@pytest.mark.asyncio
async def test_session_allready_connected(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connction failing."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_3)
    connection_callback = AsyncMock()

    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    await session.connect()
    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    with pytest.raises(AllreadyConnectedError):
        await session.connect()

    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )


@pytest.mark.asyncio
async def test_session_connection_closed(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connection."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_3)
    connection_callback = AsyncMock()

    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED

    await session.connect()

    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await appliance.ws.close()

    await asyncio.sleep(1)

    assert not session.connected
    assert session.connection_state == ConnectionState.ABNORMAL_CLOSURE
    assert session.last_close_code == 1000

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.ABNORMAL_CLOSURE),
        ]
    )

    await session.close()


@pytest.mark.asyncio
async def test_session_reconnect_manual(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connection."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()

    session = HCSession(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED
    await session.connect()
    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await appliance.ws.close()

    await asyncio.sleep(1)

    assert not session.connected
    assert session.connection_state == ConnectionState.ABNORMAL_CLOSURE
    assert session.last_close_code == 1000

    await session.connect()

    # A fresh connection makes the previous disconnect's close code stale -
    # it no longer describes the session's current state.
    assert session.last_close_code is None

    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.ABNORMAL_CLOSURE),
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )


@pytest.mark.asyncio
async def test_session_reconnect_auto(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connection."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()

    session = HCSessionReconnect(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=False,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED

    await session.connect()

    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await appliance.ws.close()

    await asyncio.sleep(0)

    assert not session.connected
    assert session.connection_state == ConnectionState.RECONNECTING
    assert session.last_close_code == 1000

    await asyncio.sleep(1)

    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED
    # A fresh connection makes the previous disconnect's close code stale -
    # it no longer describes the session's current state.
    assert session.last_close_code is None

    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.RECONNECTING),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )


@pytest.mark.asyncio
async def test_session_reconnect_auto_handshake(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """Test Session connection."""
    appliance = await appliance_server(DEVICE_MESSAGE_SET_1)
    connection_callback = AsyncMock()

    session = HCSessionReconnect(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=True,
        connection_state_callback=connection_callback,
    )

    assert not session.connected
    assert session.connection_state == ConnectionState.CLOSED

    await session.connect()

    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await appliance.ws.close()

    await asyncio.sleep(0)

    assert not session.connected
    assert session.connection_state == ConnectionState.RECONNECTING
    assert session.last_close_code == 1000

    await asyncio.sleep(1)

    assert session.connected
    assert session.connection_state == ConnectionState.CONNECTED

    await session.close()

    connection_callback.assert_has_awaits(
        [
            call(ConnectionState.CONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.RECONNECTING),
            call(ConnectionState.HANDSHAKE),
            call(ConnectionState.CONNECTED),
            call(ConnectionState.CLOSING),
            call(ConnectionState.CLOSED),
        ]
    )


@pytest.mark.asyncio
async def test_shutdown_during_active_reconnect_is_not_immediate(
    appliance_server: Callable[..., Awaitable[ApplianceServer]],
) -> None:
    """
    Regression test for homeconnect_local_hass fork issue #30's suspected cause.

    A Home Assistant config entry reload calls HomeAppliance.close(). Before
    the fix, this called session.close() (which set
    HCSessionReconnect._reconnect = False, but did NOT cancel the already-
    running background _reconnect_loop() task) and then
    TaskManager.shutdown() (which waited for that task to notice the flag
    and exit on its own, up to BLOCK_TIMEOUT seconds, before force-
    cancelling it). If the appliance was still unreachable when close() was
    called, the caller was blocked for whatever was left of the current
    backoff sleep - confirmed live against a real fake server to take ~4.8s,
    roughly RECONNECT_INITIAL_DELAY, since close() happens shortly after the
    first failed retry.

    Fixed by having HCSessionReconnect track its reconnect task and cancel
    it directly in close(), instead of relying on TaskManager.shutdown()'s
    generic wait-then-cancel-after-timeout fallback.
    """
    appliance = await appliance_server(DEVICE_MESSAGE_SET_1)
    task_manager = TaskManager()

    session = HCSessionReconnect(
        appliance.host,
        app_name=TEST_APP_NAME,
        app_id=TEST_APP_ID,
        psk64=None,
        handshake=False,
        task_manager=task_manager,
    )

    await session.connect()
    assert session.connected

    # Kill the fake server outright so every reconnect attempt genuinely
    # fails, instead of just closing the one active websocket (which the
    # fake server would happily re-accept a new connection for).
    await appliance.close_server()

    await asyncio.sleep(0.2)
    assert session.connection_state == ConnectionState.RECONNECTING

    loop = asyncio.get_running_loop()
    start = loop.time()
    # Mirrors HomeAppliance.close(): session.close() first (sets the flag),
    # then the task manager shutdown that actually waits.
    await session.close()
    await task_manager.shutdown()
    elapsed = loop.time() - start

    assert elapsed < 1, (
        f"close() took {elapsed:.2f}s to return instead of being near-"
        "instant - the background reconnect loop wasn't actually cancelled, "
        "just waited out. This reproduces the suspected #30 freeze "
        "mechanism (a HA reload blocking on this)."
    )
