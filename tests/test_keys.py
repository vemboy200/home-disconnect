import re
from enum import StrEnum

import pytest

from home_disconnect import keys

ENUMS = [
    (keys.StatusKey, "Status"),
    (keys.SettingKey, "Setting"),
    (keys.EventKey, "Event"),
    (keys.OptionKey, "Option"),
    (keys.ProgramKey, "Program"),
    (keys.CommandKey, "Command"),
    (keys.RootKey, "Root"),
]


def _upper_snake(part: str) -> str:
    part = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", part)
    part = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", part)
    return re.sub(r"([A-Za-z])([0-9])", r"\1_\2", part).upper()


def _member_name(name: str) -> str:
    parts = name.split(".")
    del parts[2]
    return "_".join(_upper_snake(part) for part in parts)


@pytest.mark.parametrize(("enum", "kind"), ENUMS)
def test_each_enum_holds_one_kind(enum: type[StrEnum], kind: str) -> None:
    for member in enum:
        assert member.value.split(".")[2] == kind, member


@pytest.mark.parametrize("enum", [enum for enum, _ in ENUMS])
def test_member_names_follow_the_feature_names(enum: type[StrEnum]) -> None:
    for member in enum:
        if member.name.endswith("_DOTTED"):
            expected = _member_name(member.value.replace(".Active", "Active")) + "_DOTTED"
        else:
            expected = _member_name(member.value)
        assert member.name == expected, member


def test_keys_work_as_names() -> None:
    names: dict[str, int] = {keys.StatusKey.BSH_COMMON_DOOR_STATE: 1}
    assert names["BSH.Common.Status.DoorState"] == 1
