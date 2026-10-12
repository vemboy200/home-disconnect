import asyncio
from collections.abc import AsyncIterator, Callable
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

import aiohttp
import pytest

from home_disconnect import appliance as appliance_module
from home_disconnect.appliance import Appliance
from home_disconnect.entities import (
    AccessError,
    DelayTooLongError,
    Entities,
    InvalidValueError,
    ProgramDurationUnknownError,
)
from home_disconnect.messages import Message, ResponseError
from home_disconnect.profile import parse_profile

DESCRIPTION = """<?xml version="1.0" encoding="UTF-8"?>
<device xmlns="http://www.home-connect.com/schemas/DeviceDescription/20140417">
  <description><type>Washer</type><brand>TEST</brand><model>WM1</model></description>
  <settingList access="readWrite" available="true" uid="0103">
    <setting access="readWrite" available="true" refCID="1A" refDID="8B" uid="0208"/>
    <setting access="readWrite" available="true" refCID="01" refDID="00" uid="0300"/>
    <setting access="readWrite" available="true" refCID="10" refDID="82" min="10" max="100"
             uid="0301"/>
  </settingList>
  <optionList access="readWrite" available="true" uid="0106">
    <option access="readWrite" available="true" refCID="10" refDID="82" min="0" max="86400"
            uid="0229"/>
    <option access="readWrite" available="true" refCID="10" refDID="82" min="0" max="86400"
            uid="022A"/>
    <option access="read" available="true" refCID="10" refDID="82" uid="022B"/>
  </optionList>
  <programGroup available="true" uid="0107">
    <program available="true" execution="selectAndStart" uid="2001"/>
  </programGroup>
  <activeProgram access="read" uid="0100"/>
  <selectedProgram access="readWrite" uid="0101"/>
</device>
"""

FEATURE_MAPPING = """<?xml version="1.0" encoding="UTF-8"?>
<featureMappingFile xmlns="http://www.home-connect.com/schemas/FeatureMapping/20140417">
  <featureDescription>
    <feature refUID="0100">BSH.Common.Root.ActiveProgram</feature>
    <feature refUID="0101">BSH.Common.Root.SelectedProgram</feature>
    <feature refUID="0208">BSH.Common.Setting.ApplianceDateTime</feature>
    <feature refUID="0300">Cooking.Common.Setting.Lighting</feature>
    <feature refUID="0301">Cooking.Common.Setting.LightingBrightness</feature>
    <feature refUID="0229">BSH.Common.Option.StartInRelative</feature>
    <feature refUID="022A">BSH.Common.Option.FinishInRelative</feature>
    <feature refUID="022B">BSH.Common.Option.EstimatedTotalProgramTime</feature>
    <feature refUID="2001">LaundryCare.Washer.Program.Cotton</feature>
  </featureDescription>
</featureMappingFile>
"""

CLOCK, LIGHT, BRIGHTNESS, START_IN, FINISH_IN = 0x0208, 0x0300, 0x0301, 0x0229, 0x022A
ESTIMATE = 0x022B
ACTIVE, SELECTED, COTTON = 0x0100, 0x0101, 0x2001


class Recorder:
    def __init__(self) -> None:
        self.sent: list[tuple[str, Any]] = []
        self.refuse: Callable[[Message], int | None] = lambda _: None

    async def __call__(self, message: Message) -> Message:
        self.sent.append((message.resource, message.data))
        code = self.refuse(message)
        if code is not None:
            raise ResponseError(code, message.resource)
        return message.response()


@pytest.fixture
def recorder() -> Recorder:
    return Recorder()


def make_appliance(
    client_session: aiohttp.ClientSession, recorder: Recorder, description: str = DESCRIPTION
) -> Appliance:
    profile = parse_profile(description, FEATURE_MAPPING)
    test_appliance = Appliance(
        client_session, "127.0.0.1", profile, "AAAA", app_name="Test", app_id="id"
    )
    # No connection: requests go to the recorder.
    test_appliance.session.request = recorder  # type: ignore[method-assign]
    test_appliance.entities = Entities(profile, recorder)
    return test_appliance


@pytest.fixture
async def appliance(recorder: Recorder) -> AsyncIterator[Appliance]:
    async with aiohttp.ClientSession() as client_session:
        yield make_appliance(client_session, recorder)


@pytest.fixture
async def finish_in_only(recorder: Recorder) -> AsyncIterator[Appliance]:
    """An appliance that takes a delay only as a finish time (no StartInRelative)."""
    start_in = (
        '    <option access="readWrite" available="true" refCID="10" refDID="82" min="0"'
        ' max="86400"\n            uid="0229"/>\n'
    )
    assert start_in in DESCRIPTION
    async with aiohttp.ClientSession() as client_session:
        test_appliance = make_appliance(client_session, recorder, DESCRIPTION.replace(start_in, ""))
        test_appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
        yield test_appliance


def started_options(recorder: Recorder) -> list[dict[str, Any]]:
    [(resource, data)] = recorder.sent
    assert resource == "/ro/activeProgram"
    return data[0]["options"]


async def test_set_values_in_one_message(appliance: Appliance, recorder: Recorder) -> None:
    await appliance.set_values({"Cooking.Common.Setting.Lighting": True, BRIGHTNESS: 80})
    assert recorder.sent == [
        ("/ro/values", [{"uid": LIGHT, "value": True}, {"uid": BRIGHTNESS, "value": 80}])
    ]
    await appliance.set_values({})
    assert len(recorder.sent) == 1


async def test_set_values_checks_every_value_first(
    appliance: Appliance, recorder: Recorder
) -> None:
    with pytest.raises(InvalidValueError, match="above the maximum"):
        await appliance.set_values({LIGHT: True, BRIGHTNESS: 150})
    appliance.entities.apply([{"uid": BRIGHTNESS, "access": "read"}])
    with pytest.raises(AccessError):
        await appliance.set_values({LIGHT: True, BRIGHTNESS: 50})
    with pytest.raises(AccessError, match=r"has no Not\.There"):
        await appliance.set_values({"Not.There": 1})
    assert recorder.sent == []


@pytest.mark.parametrize(
    "when",
    [
        datetime(2026, 9, 27, 21, 5, 9, 123456),  # noqa: DTZ001 - naive local time
        datetime(2026, 9, 27, 21, 5, 9, tzinfo=timezone(timedelta(hours=-7))),
        datetime(2026, 9, 27, 21, 5, 9, tzinfo=UTC),
    ],
)
async def test_set_datetime_sends_naive_local_time(
    appliance: Appliance, recorder: Recorder, when: datetime
) -> None:
    await appliance.set_datetime(when)
    assert recorder.sent == [("/ro/values", [{"uid": CLOCK, "value": "2026-09-27T21:05:09"}])]


async def test_set_start_in(appliance: Appliance, recorder: Recorder) -> None:
    await appliance.set_start_in(3600)
    assert recorder.sent == [("/ro/values", [{"uid": START_IN, "value": 3600}])]


async def test_set_finish_in_directly(appliance: Appliance, recorder: Recorder) -> None:
    await appliance.set_finish_in(7200)
    assert recorder.sent == [("/ro/values", [{"uid": FINISH_IN, "value": 7200}])]


async def test_set_finish_in_falls_back_to_the_active_program_window(
    appliance: Appliance, recorder: Recorder
) -> None:
    # Fork issue #384's dryer: FinishInRelative alone is refused, and the active program
    # only becomes writable for a moment.
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    recorder.refuse = lambda m: 541 if m.data == [{"uid": FINISH_IN, "value": 7200}] else None
    active = appliance.entities.by_uid[ACTIVE]

    async def open_window() -> None:
        await asyncio.sleep(0.05)
        for changed in appliance.entities.apply([{"uid": ACTIVE, "access": "readWrite"}]):
            await changed.run_callbacks()

    opener = asyncio.create_task(open_window())
    await appliance.set_finish_in(7200)
    await opener
    assert recorder.sent == [
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}]),
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}, {"uid": ACTIVE, "value": COTTON}]),
    ]
    assert active.access is not None
    assert active.access.writable


async def test_set_finish_in_other_errors_are_raised(
    appliance: Appliance, recorder: Recorder
) -> None:
    recorder.refuse = lambda _: 400
    with pytest.raises(ResponseError):
        await appliance.set_finish_in(7200)
    assert len(recorder.sent) == 1


async def test_set_finish_in_fallback_needs_a_program(
    appliance: Appliance, recorder: Recorder
) -> None:
    recorder.refuse = lambda _: 501
    with pytest.raises(AccessError, match="No program is selected"):
        await appliance.set_finish_in(7200)


START_WITH_FINISH_IN = (
    "/ro/activeProgram",
    [{"program": COTTON, "options": [{"uid": FINISH_IN, "value": 7200}]}],
)


async def test_set_finish_in_starts_the_program_when_no_window_opens(
    appliance: Appliance, recorder: Recorder, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Fork issue #146's washer: the active program never becomes writable, but a program
    # start with the finish time as an option is accepted.
    monkeypatch.setattr(appliance_module, "ACTIVE_PROGRAM_WINDOW", 0.05)
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    recorder.refuse = lambda m: 541 if m.resource == "/ro/values" else None
    await appliance.set_finish_in(7200)
    assert recorder.sent == [
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}]),
        START_WITH_FINISH_IN,
    ]


async def test_set_finish_in_fallback_gives_up_when_no_window_opens(
    appliance: Appliance, recorder: Recorder, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(appliance_module, "ACTIVE_PROGRAM_WINDOW", 0.05)
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    recorder.refuse = lambda _: 541
    with pytest.raises(AccessError, match="didn't open a window"):
        await appliance.set_finish_in(7200)
    assert recorder.sent == [
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}]),
        START_WITH_FINISH_IN,
    ]


async def open_active_program_window(appliance: Appliance) -> None:
    await asyncio.sleep(0.05)
    for changed in appliance.entities.apply([{"uid": ACTIVE, "access": "readWrite"}]):
        await changed.run_callbacks()


async def test_set_finish_in_starts_the_program_when_the_combined_write_is_refused(
    appliance: Appliance, recorder: Recorder
) -> None:
    # Fork issue #146's washer refuses both writes with 541 and only takes the start.
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    recorder.refuse = lambda m: 541 if m.resource == "/ro/values" else None
    opener = asyncio.create_task(open_active_program_window(appliance))
    await appliance.set_finish_in(7200)
    await opener
    assert recorder.sent == [
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}]),
        ("/ro/values", [{"uid": FINISH_IN, "value": 7200}, {"uid": ACTIVE, "value": COTTON}]),
        START_WITH_FINISH_IN,
    ]


async def test_set_finish_in_combined_write_other_errors_are_raised(
    appliance: Appliance, recorder: Recorder
) -> None:
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    recorder.refuse = lambda m: 400 if m.data and len(m.data) > 1 else 541
    opener = asyncio.create_task(open_active_program_window(appliance))
    with pytest.raises(ResponseError):
        await appliance.set_finish_in(7200)
    await opener
    assert len(recorder.sent) == 2  # noqa: PLR2004


async def test_wait_until_writable_returns_at_once_when_writable(appliance: Appliance) -> None:
    async with asyncio.timeout(1):
        await appliance.entities.by_uid[LIGHT].wait_until_writable()


CLOUD_DESCRIPTION = DESCRIPTION.replace(
    "  </settingList>",
    '    <setting access="readWrite" available="true" refCID="01" refDID="00" uid="0003"/>\n'
    "  </settingList>\n"
    '  <statusList access="read" available="true" uid="0102">\n'
    '    <status access="read" available="true" refCID="01" refDID="00" uid="0005"/>\n'
    "  </statusList>",
)
CLOUD_MAPPING = FEATURE_MAPPING.replace(
    "  </featureDescription>",
    '    <feature refUID="0003">BSH.Common.Setting.AllowBackendConnection</feature>\n'
    '    <feature refUID="0005">BSH.Common.Status.BackendConnected</feature>\n'
    "  </featureDescription>",
)


async def test_cloud_connection(appliance: Appliance, recorder: Recorder) -> None:
    # Without the setting, there's nothing to toggle.
    assert appliance.cloud_connection_allowed is None
    assert appliance.cloud_connected is None
    with pytest.raises(AccessError, match="AllowBackendConnection"):
        await appliance.set_cloud_connection(allowed=False)

    appliance.entities = Entities(parse_profile(CLOUD_DESCRIPTION, CLOUD_MAPPING), recorder)
    appliance.entities.apply([{"uid": 0x0003, "value": True}, {"uid": 0x0005, "value": 1}])
    assert appliance.cloud_connection_allowed is True
    assert appliance.cloud_connected is True
    await appliance.set_cloud_connection(allowed=False)
    assert recorder.sent == [("/ro/values", [{"uid": 0x0003, "value": False}])]


async def test_set_values_raw_skips_checks(appliance: Appliance, recorder: Recorder) -> None:
    appliance.entities.apply([{"uid": BRIGHTNESS, "access": "read"}])
    await appliance.set_values_raw({LIGHT: 1, BRIGHTNESS: 150})
    await appliance.set_values_raw({})
    assert recorder.sent == [
        ("/ro/values", [{"uid": LIGHT, "value": 1}, {"uid": BRIGHTNESS, "value": 150}])
    ]


async def test_start_delay_goes_into_start_in(appliance: Appliance, recorder: Recorder) -> None:
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    await appliance.start_program(delay=3600)
    assert started_options(recorder) == [{"uid": START_IN, "value": 3600}]


async def test_start_delay_as_finish_time_adds_the_estimate(
    finish_in_only: Appliance, recorder: Recorder
) -> None:
    # FinishInRelative may hold an earlier finish time; the estimate is the duration.
    finish_in_only.entities.apply(
        [{"uid": ESTIMATE, "value": 5400}, {"uid": FINISH_IN, "value": 9000}]
    )
    await finish_in_only.start_program(delay=3600)
    assert started_options(recorder) == [{"uid": FINISH_IN, "value": 9000}]


async def test_start_delay_as_finish_time_falls_back_to_finish_in(
    finish_in_only: Appliance, recorder: Recorder
) -> None:
    # Fork issue #146: a washer that reports the duration as FinishInRelative.
    finish_in_only.entities.apply(
        [{"uid": ESTIMATE, "available": False, "value": 5400}, {"uid": FINISH_IN, "value": 3600}]
    )
    await finish_in_only.start_program(delay=7200)
    assert started_options(recorder) == [{"uid": FINISH_IN, "value": 10800}]


async def test_start_delay_uses_a_finish_time_given_as_an_option(
    finish_in_only: Appliance, recorder: Recorder
) -> None:
    await finish_in_only.start_program(options={FINISH_IN: 1800}, delay=3600)
    assert started_options(recorder) == [{"uid": FINISH_IN, "value": 5400}]


async def test_start_delay_problems_send_nothing(
    appliance: Appliance, finish_in_only: Appliance, recorder: Recorder
) -> None:
    appliance.entities.apply([{"uid": SELECTED, "value": COTTON}])
    with pytest.raises(DelayTooLongError) as err:
        await appliance.start_program(delay=86401)
    assert err.value.maximum == 86400  # noqa: PLR2004

    with pytest.raises(ProgramDurationUnknownError):
        await finish_in_only.start_program(delay=3600)

    finish_in_only.entities.apply([{"uid": ESTIMATE, "value": 80000}])
    with pytest.raises(DelayTooLongError):
        await finish_in_only.start_program(delay=7200)
    assert recorder.sent == []
