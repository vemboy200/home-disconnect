"""Local WebSocket client for Home Connect appliances."""

from importlib.metadata import PackageNotFoundError, version

from .account import AccountError, SignIn, Token, fetch_profiles
from .appliance import Appliance
from .entities import (
    Access,
    AccessError,
    ActiveProgram,
    Command,
    DelayTooLongError,
    Entities,
    Entity,
    Event,
    Execution,
    InvalidValueError,
    Option,
    Program,
    ProgramDurationUnknownError,
    RemoteStartNotAllowedError,
    SelectedProgram,
    Setting,
    Status,
)
from .errors import (
    AlreadyConnectedError,
    AuthenticationError,
    ConnectionClosedError,
    ConnectionFailedError,
    DecryptionError,
    HomeDisconnectError,
)
from .keys import (
    CommandKey,
    EventKey,
    OptionKey,
    ProgramKey,
    RootKey,
    SettingKey,
    StatusKey,
)
from .legacy import serialize_legacy_description
from .messages import Action, Message, ResponseError
from .profile import DeviceProfile, ProfileError, parse_profile
from .profile_files import (
    LoadedProfile,
    build_profile_zip,
    load_profiles,
    load_profiles_from_zip,
    profile_filename_stub,
)
from .session import ConnectionState, HandshakeError, Session
from .transport import appliance_hostname

try:
    __version__ = version("home-disconnect")
except PackageNotFoundError:  # pragma: no cover - running from a source tree without an install
    __version__ = "0.0.0"

__all__ = [
    "Access",
    "AccessError",
    "AccountError",
    "Action",
    "ActiveProgram",
    "AlreadyConnectedError",
    "Appliance",
    "AuthenticationError",
    "Command",
    "CommandKey",
    "ConnectionClosedError",
    "ConnectionFailedError",
    "ConnectionState",
    "DecryptionError",
    "DelayTooLongError",
    "DeviceProfile",
    "Entities",
    "Entity",
    "Event",
    "EventKey",
    "Execution",
    "HandshakeError",
    "HomeDisconnectError",
    "InvalidValueError",
    "LoadedProfile",
    "Message",
    "Option",
    "OptionKey",
    "ProfileError",
    "Program",
    "ProgramDurationUnknownError",
    "ProgramKey",
    "RemoteStartNotAllowedError",
    "ResponseError",
    "RootKey",
    "SelectedProgram",
    "Session",
    "Setting",
    "SettingKey",
    "SignIn",
    "Status",
    "StatusKey",
    "Token",
    "__version__",
    "appliance_hostname",
    "build_profile_zip",
    "fetch_profiles",
    "load_profiles",
    "load_profiles_from_zip",
    "parse_profile",
    "profile_filename_stub",
    "serialize_legacy_description",
]
