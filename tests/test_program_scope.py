"""Option description changes scoped to a program (`parentUID`).

The message sequences follow a Bosch HMG936AB1 oven, on the dishwasher profile of the
fixtures: Eco50 and Quick45 are the programs, Duration is an option.
"""

import pytest

from home_disconnect.entities import Access, Entities, Option
from home_disconnect.messages import Message
from home_disconnect.profile import parse_profile

from .profile_fixtures import DESCRIPTION, FEATURE_MAPPING

DOOR = "BSH.Common.Status.DoorState"
ABORT = "BSH.Common.Command.AbortProgram"
DURATION = "BSH.Common.Option.Duration"
ECO = "Dishcare.Dishwasher.Program.Eco50"
QUICK = "Dishcare.Dishwasher.Program.Quick45"

SCOPED_MAX = 99
OLD_VALUE = 3555
CURRENT_VALUE = 10
GLOBAL_MAX = 250
GLOBAL_MIN = 5
STEP = 5


async def _send(message: Message) -> Message:
    return message.response()


@pytest.fixture
def entities() -> Entities:
    return Entities(parse_profile(DESCRIPTION, FEATURE_MAPPING), _send)


def _uids(entities: Entities) -> tuple[Option, int, int, int, int]:
    duration = entities[DURATION]
    assert isinstance(duration, Option)
    assert entities.selected_program is not None
    assert entities.active_program is not None
    return (
        duration,
        entities.programs[ECO].uid,
        entities.programs[QUICK].uid,
        entities.selected_program.uid,
        entities.active_program.uid,
    )


def test_change_for_another_program_is_not_applied(entities: Entities) -> None:
    duration, _, quick, _, _ = _uids(entities)
    before = (duration.access, duration.available)

    # The HMG936AB1 sends this for an empty favorite on every connect
    changed = entities.apply(
        [{"uid": duration.uid, "parentUID": quick, "available": False, "access": "READ"}]
    )

    assert changed == []
    assert (duration.access, duration.available) == before


def test_change_for_the_selected_program_is_applied(entities: Entities) -> None:
    duration, eco, _, selected, _ = _uids(entities)

    entities.apply([{"uid": selected, "value": eco}])
    changed = entities.apply([{"uid": duration.uid, "parentUID": eco, "access": "READ"}])

    assert changed == [duration]
    assert duration.access is Access.READ


def test_change_for_the_active_program_is_applied(entities: Entities) -> None:
    duration, eco, _, _, active = _uids(entities)

    entities.apply([{"uid": active, "value": eco}])
    entities.apply([{"uid": duration.uid, "parentUID": eco, "available": False}])

    assert duration.available is False


def test_change_is_applied_once_its_program_is_selected(entities: Entities) -> None:
    """`/ro/allDescriptionChanges` arrives before `/ro/allMandatoryValues`."""
    duration, eco, _, selected, _ = _uids(entities)

    entities.apply([{"uid": duration.uid, "parentUID": eco, "access": "READ", "max": SCOPED_MAX}])
    assert (duration.access, duration.max) != (Access.READ, SCOPED_MAX)

    changed = entities.apply([{"uid": selected, "value": eco}])

    assert duration in changed
    assert (duration.access, duration.max) == (Access.READ, SCOPED_MAX)


def test_value_for_another_program_is_never_applied(entities: Entities) -> None:
    duration, eco, _, selected, _ = _uids(entities)
    entities.apply([{"uid": duration.uid, "value": CURRENT_VALUE}])

    entities.apply([{"uid": duration.uid, "parentUID": eco, "available": True, "value": OLD_VALUE}])
    assert duration.value_raw == CURRENT_VALUE

    entities.apply([{"uid": selected, "value": eco}])
    assert duration.value_raw == CURRENT_VALUE


def test_selecting_another_program(entities: Entities) -> None:
    """The selected program changes first, then come changes for the new and the old one."""
    duration, eco, quick, selected, _ = _uids(entities)
    entities.apply([{"uid": selected, "value": eco}])

    entities.apply([{"uid": selected, "value": quick}])
    entities.apply(
        [
            {"uid": duration.uid, "parentUID": quick, "available": False},
            {"uid": duration.uid, "parentUID": eco, "available": True, "value": OLD_VALUE},
        ]
    )

    assert duration.available is False


def test_changes_without_a_program_scope_are_applied(entities: Entities) -> None:
    duration, eco, _, _, _ = _uids(entities)
    door = entities[DOOR]
    abort = entities[ABORT]

    entities.apply(
        [
            {"uid": duration.uid, "max": GLOBAL_MAX},  # no parentUID
            {"uid": duration.uid, "parentUID": 0, "min": GLOBAL_MIN},  # parentUID 0
            {"uid": duration.uid, "parentUID": door.uid, "stepSize": STEP},  # parent: no program
            {"uid": abort.uid, "parentUID": eco, "available": False},  # not an option
        ]
    )

    assert (duration.max, duration.min, duration.step) == (GLOBAL_MAX, GLOBAL_MIN, STEP)
    assert abort.available is False


def test_invalid_parent_uid_is_not_program_scoped(entities: Entities) -> None:
    duration, _, _, _, _ = _uids(entities)

    entities.apply([{"uid": duration.uid, "parentUID": "not a uid", "available": False}])

    assert duration.available is False


def test_value_only_change_for_another_program_is_not_remembered(entities: Entities) -> None:
    duration, eco, _, selected, _ = _uids(entities)
    entities.apply([{"uid": duration.uid, "value": CURRENT_VALUE}])

    entities.apply([{"uid": duration.uid, "parentUID": eco, "value": OLD_VALUE}])
    changed = entities.apply([{"uid": selected, "value": eco}])

    assert duration not in changed
    assert duration.value_raw == CURRENT_VALUE


def test_option_restored_and_changed_in_one_message(entities: Entities) -> None:
    duration, eco, _, selected, _ = _uids(entities)
    entities.apply([{"uid": duration.uid, "parentUID": eco, "access": "READ"}])

    changed = entities.apply(
        [
            {"uid": duration.uid, "value": CURRENT_VALUE},
            {"uid": selected, "value": eco},
        ]
    )

    assert changed.count(duration) == 1
    assert duration.access is Access.READ


def test_reported_program_again_keeps_a_newer_change(entities: Entities) -> None:
    duration, eco, _, selected, _ = _uids(entities)
    entities.apply([{"uid": selected, "value": eco}])
    entities.apply([{"uid": duration.uid, "parentUID": eco, "access": "READ"}])
    entities.apply([{"uid": duration.uid, "access": "READWRITE"}])

    changed = entities.apply([{"uid": selected, "value": eco}])

    assert duration not in changed
    assert duration.access is Access.READ_WRITE


def test_starting_the_selected_program_keeps_a_newer_change(entities: Entities) -> None:
    duration, eco, _, selected, active = _uids(entities)
    entities.apply([{"uid": selected, "value": eco}])
    entities.apply([{"uid": duration.uid, "parentUID": eco, "access": "READ"}])
    entities.apply([{"uid": duration.uid, "access": "READWRITE"}])

    changed = entities.apply([{"uid": active, "value": eco}])

    assert duration not in changed
    assert duration.access is Access.READ_WRITE
