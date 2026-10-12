from collections.abc import AsyncIterator
from typing import Any

import aiohttp
import pytest

from home_disconnect.appliance import Appliance
from home_disconnect.entities import AccessError, Entities
from home_disconnect.messages import Message
from home_disconnect.profile import parse_profile

DESCRIPTION = """<?xml version="1.0" encoding="UTF-8"?>
<device xmlns="http://www.home-connect.com/schemas/DeviceDescription/20140417">
  <description><type>Hood</type><brand>TEST</brand><model>DWK1</model></description>
  <settingList access="readWrite" available="true" uid="0103">
    <setting access="readWrite" available="true" enumerationType="1001" refCID="03"
             refDID="80" min="1" max="2" uid="0539"/>
  </settingList>
  <optionList access="readWrite" available="true" uid="0106">
    <option access="readWrite" available="true" enumerationType="D80C" refCID="03"
            refDID="80" uid="D80C"/>
    <option access="readWrite" available="true" enumerationType="D809" refCID="03"
            refDID="80" uid="D809"/>
    <option access="readWrite" available="true" refCID="01" refDID="00" uid="D801"/>
  </optionList>
  <programGroup available="true" uid="0107">
    <program available="true" execution="startOnly" uid="D80B">
      <option access="readWrite" available="true" refUID="D80C"/>
      <option access="readWrite" available="true" refUID="D809"/>
      <option access="readWrite" available="true" refUID="D801"/>
    </program>
    <program available="true" execution="startOnly" uid="D80A">
      <option access="readWrite" available="true" refUID="D80C"/>
    </program>
  </programGroup>
  <activeProgram access="readWrite" uid="0100"/>
  <selectedProgram access="read" fullOptionSet="false" uid="0101"/>
  <enumerationTypeList>
    <enumerationType enid="1001"><enumeration value="1"/><enumeration value="2"/>
      <enumeration value="3"/></enumerationType>
    <enumerationType enid="D80C"><enumeration value="0"/><enumeration value="1"/>
      <enumeration value="2"/></enumerationType>
    <enumerationType enid="D809"><enumeration value="0"/><enumeration value="1"/>
      </enumerationType>
  </enumerationTypeList>
</device>
"""

FEATURE_MAPPING = """<?xml version="1.0" encoding="UTF-8"?>
<featureMappingFile xmlns="http://www.home-connect.com/schemas/FeatureMapping/20140417">
  <featureDescription>
    <feature refUID="0100">BSH.Common.Root.ActiveProgram</feature>
    <feature refUID="0101">BSH.Common.Root.SelectedProgram</feature>
    <feature refUID="0539">BSH.Common.Setting.PowerState</feature>
    <feature refUID="D80C">Cooking.Common.Option.Hood.VentingLevel</feature>
    <feature refUID="D809">Cooking.Common.Option.Hood.IntensiveLevel</feature>
    <feature refUID="D801">Cooking.Common.Option.Hood.Boost</feature>
    <feature refUID="D80B">Cooking.Common.Program.Hood.Venting</feature>
    <feature refUID="D80A">Cooking.Common.Program.Hood.Automatic</feature>
  </featureDescription>
  <enumDescriptionList>
    <enumDescription refENID="1001" enumKey="BSH.Common.EnumType.PowerState">
      <enumMember refValue="1">Off</enumMember><enumMember refValue="2">On</enumMember>
      <enumMember refValue="3">Standby</enumMember>
    </enumDescription>
    <enumDescription refENID="D80C" enumKey="Cooking.Hood.EnumType.Stage.FanStage">
      <enumMember refValue="0">FanOff</enumMember><enumMember refValue="1">FanStage01</enumMember>
      <enumMember refValue="2">FanStage02</enumMember>
    </enumDescription>
    <enumDescription refENID="D809" enumKey="Cooking.Hood.EnumType.IntensiveStage">
      <enumMember refValue="0">IntensiveStageOff</enumMember>
      <enumMember refValue="1">IntensiveStage1</enumMember>
    </enumDescription>
  </enumDescriptionList>
</featureMappingFile>
"""

POWER, LEVEL, INTENSIVE, BOOST = 0x0539, 0xD80C, 0xD809, 0xD801
VENTING, AUTOMATIC, ACTIVE = 0xD80B, 0xD80A, 0x0100


class Recorder:
    def __init__(self) -> None:
        self.sent: list[tuple[str, Any]] = []

    async def __call__(self, message: Message) -> Message:
        self.sent.append((message.resource, message.data))
        return message.response()


@pytest.fixture
def recorder() -> Recorder:
    return Recorder()


def make_hood(
    client_session: aiohttp.ClientSession, recorder: Recorder, description: str
) -> Appliance:
    profile = parse_profile(description, FEATURE_MAPPING)
    hood = Appliance(client_session, "127.0.0.1", profile, "AAAA", app_name="Test", app_id="id")
    hood.session.request = recorder  # type: ignore[method-assign]
    hood.entities = Entities(profile, recorder)
    return hood


@pytest.fixture
async def hood(recorder: Recorder) -> AsyncIterator[Appliance]:
    async with aiohttp.ClientSession() as client_session:
        yield make_hood(client_session, recorder, DESCRIPTION)


def started(recorder: Recorder) -> tuple[int, dict[int, Any]]:
    [(resource, data)] = recorder.sent
    assert resource == "/ro/activeProgram"
    return data[0]["program"], {item["uid"]: item["value"] for item in data[0]["options"]}


async def test_fan_level_turns_the_other_level_off(hood: Appliance, recorder: Recorder) -> None:
    await hood.set_fan_level("Cooking.Common.Option.Hood.VentingLevel", "FanStage02")
    assert started(recorder) == (VENTING, {LEVEL: 2, INTENSIVE: 0})


async def test_fan_level_in_the_running_program(hood: Appliance, recorder: Recorder) -> None:
    # Automatic only takes the venting level, so the intensive level isn't sent.
    hood.entities.apply([{"uid": ACTIVE, "value": AUTOMATIC}])
    await hood.set_fan_level(LEVEL, 1)
    assert started(recorder) == (AUTOMATIC, {LEVEL: 1})
    with pytest.raises(AccessError):
        await hood.set_fan_level(INTENSIVE, "IntensiveStage1")


async def test_start_fan_and_boost(hood: Appliance, recorder: Recorder) -> None:
    await hood.start_fan()
    await hood.set_boost(on=True)
    await hood.set_boost(on=False)
    sent = [(data[0]["program"], data[0]["options"]) for _, data in recorder.sent]
    assert sent == [
        (VENTING, []),
        (
            VENTING,
            [
                {"uid": LEVEL, "value": 0},
                {"uid": BOOST, "value": True},
                {"uid": INTENSIVE, "value": 0},
            ],
        ),
        (VENTING, []),
    ]


async def test_power_off_uses_a_writable_off_state(hood: Appliance, recorder: Recorder) -> None:
    await hood.power_off()
    assert recorder.sent == [("/ro/values", [{"uid": POWER, "value": 1}])]


async def test_power_off_without_an_off_state(recorder: Recorder) -> None:
    # Off is declared but outside the writable range (2 to 3).
    description = DESCRIPTION.replace('min="1" max="2"', 'min="2" max="3"')
    async with aiohttp.ClientSession() as client_session:
        hood = make_hood(client_session, recorder, description)
        with pytest.raises(AccessError):
            await hood.power_off()
    assert recorder.sent == []


async def test_fan_ignores_the_remote_start_status(recorder: Recorder) -> None:
    # The Start button's remote start check isn't known to apply to a hood's fan.
    status = (
        '  <statusList access="read" available="true" uid="0102">\n'
        '    <status access="read" available="true" refCID="01" refDID="00" uid="0207"/>\n'
        "  </statusList>\n"
    )
    description = DESCRIPTION.replace("  <optionList", status + "  <optionList", 1)
    mapping_line = (
        '    <feature refUID="0207">BSH.Common.Status.RemoteControlStartAllowed</feature>\n'
    )
    mapping = FEATURE_MAPPING.replace(
        "  </featureDescription>", mapping_line + "  </featureDescription>"
    )
    async with aiohttp.ClientSession() as client_session:
        profile = parse_profile(description, mapping)
        hood = Appliance(client_session, "127.0.0.1", profile, "AAAA", app_name="Test", app_id="id")
        hood.session.request = recorder  # type: ignore[method-assign]
        hood.entities = Entities(profile, recorder)
        hood.entities.apply([{"uid": 0x0207, "value": False}])
        await hood.set_fan_level(LEVEL, 1)
        await hood.start_fan()
    assert len(recorder.sent) == 2  # noqa: PLR2004
