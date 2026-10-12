import asyncio
from collections.abc import AsyncIterator
from typing import Any

import aiohttp
import pytest

from home_disconnect import appliance as appliance_module
from home_disconnect.appliance import Appliance
from home_disconnect.entities import AccessError, Entities, InvalidValueError
from home_disconnect.messages import Message
from home_disconnect.profile import parse_profile

DESCRIPTION = """<?xml version="1.0" encoding="UTF-8"?>
<device xmlns="http://www.home-connect.com/schemas/DeviceDescription/20140417">
  <description><type>Hood</type><brand>TEST</brand><model>LC1</model></description>
  <settingList access="readWrite" available="true" uid="0103">
    <setting access="readWrite" available="true" refCID="01" refDID="00" uid="0400"/>
    <setting access="readWrite" available="false" refCID="10" refDID="82" min="1" max="100"
             uid="0401"/>
    <setting access="readWrite" available="false" enumerationType="0402" refCID="03"
             refDID="80" uid="0402"/>
    <setting access="readWrite" available="false" refCID="11" refDID="A1" uid="0403"/>
  </settingList>
  <enumerationTypeList>
    <enumerationType enid="0402"><enumeration value="0"/><enumeration value="1"/>
      <enumeration value="99"/></enumerationType>
  </enumerationTypeList>
</device>
"""

FEATURE_MAPPING = """<?xml version="1.0" encoding="UTF-8"?>
<featureMappingFile xmlns="http://www.home-connect.com/schemas/FeatureMapping/20140417">
  <featureDescription>
    <feature refUID="0400">BSH.Common.Setting.AmbientLightEnabled</feature>
    <feature refUID="0401">BSH.Common.Setting.AmbientLightBrightness</feature>
    <feature refUID="0402">BSH.Common.Setting.AmbientLightColor</feature>
    <feature refUID="0403">BSH.Common.Setting.AmbientLightCustomColor</feature>
  </featureDescription>
  <enumDescriptionList>
    <enumDescription refENID="0402" enumKey="BSH.Common.EnumType.AmbientLightColor">
      <enumMember refValue="0">CustomColor</enumMember>
      <enumMember refValue="1">Color1</enumMember>
      <enumMember refValue="99">Color99</enumMember>
    </enumDescription>
  </enumDescriptionList>
</featureMappingFile>
"""

ENABLED, BRIGHTNESS, MODE, CUSTOM = 0x0400, 0x0401, 0x0402, 0x0403


class Hood:
    """Answers writes like the LC91KWW60/04 from upstream #477."""

    def __init__(self) -> None:
        self.sent: list[list[dict[str, Any]]] = []
        self.entities: Entities | None = None
        self.custom_color_needs_mode = True

    async def __call__(self, message: Message) -> Message:
        data = list(message.data or [])
        self.sent.append(data)
        written = {item["uid"]: item["value"] for item in data}
        assert self.entities is not None
        if written.get(ENABLED) is True:
            # Power-on: the color settings appear shortly after the write is answered.
            asyncio.get_running_loop().call_later(0.01, self._lights_on)
        if written.get(MODE) == 0:
            asyncio.get_running_loop().call_later(
                0.01,
                lambda: self._apply(
                    [{"uid": MODE, "value": 0}, {"uid": CUSTOM, "available": True}]
                ),
            )
        return message.response()

    def _lights_on(self) -> None:
        changes = [
            {"uid": BRIGHTNESS, "available": True},
            {"uid": MODE, "available": True},
        ]
        mode = self.entities.by_uid[MODE].value_raw if self.entities else None
        if not self.custom_color_needs_mode or mode == 0:
            changes.append({"uid": CUSTOM, "available": True})
        self._apply(changes)

    def _apply(self, changes: list[dict[str, Any]]) -> None:
        assert self.entities is not None
        asyncio.ensure_future(self._run(changes))  # noqa: RUF006

    async def _run(self, changes: list[dict[str, Any]]) -> None:
        assert self.entities is not None
        for entity in self.entities.apply(changes):
            await entity.run_callbacks()


@pytest.fixture
def hood() -> Hood:
    return Hood()


@pytest.fixture
async def appliance(hood: Hood) -> AsyncIterator[Appliance]:
    async with aiohttp.ClientSession() as client_session:
        profile = parse_profile(DESCRIPTION, FEATURE_MAPPING)
        test_appliance = Appliance(
            client_session, "127.0.0.1", profile, "AAAA", app_name="Test", app_id="id"
        )
        test_appliance.session.request = hood  # type: ignore[method-assign]
        test_appliance.entities = Entities(profile, hood)
        hood.entities = test_appliance.entities
        yield test_appliance


def off(appliance: Appliance, mode: int) -> None:
    appliance.entities.apply([{"uid": ENABLED, "value": False}, {"uid": MODE, "value": mode}])


async def test_color_from_off_with_a_preset_selected(appliance: Appliance, hood: Hood) -> None:
    # The custom color only appears once CustomColor is selected, after power-on.
    off(appliance, mode=1)
    await appliance.set_ambient_light(color=(255, 128, 0))
    assert hood.sent == [
        [{"uid": ENABLED, "value": True}],
        [{"uid": MODE, "value": 0}],
        [{"uid": CUSTOM, "value": "#ff8000"}],
    ]


async def test_color_with_the_custom_color_offered(appliance: Appliance, hood: Hood) -> None:
    hood.custom_color_needs_mode = False
    off(appliance, mode=1)
    await appliance.set_ambient_light(color=(0, 0, 128))
    assert hood.sent == [
        [{"uid": ENABLED, "value": True}],
        [{"uid": CUSTOM, "value": "#000080"}, {"uid": MODE, "value": 0}],
    ]


async def test_brightness_of_a_preset(appliance: Appliance, hood: Hood) -> None:
    off(appliance, mode=1)
    await appliance.set_ambient_light(brightness=40)
    assert hood.sent == [[{"uid": ENABLED, "value": True}], [{"uid": BRIGHTNESS, "value": 40}]]


async def test_plain_turn_on_and_already_on(appliance: Appliance, hood: Hood) -> None:
    off(appliance, mode=0)
    await appliance.set_ambient_light()
    assert hood.sent == [[{"uid": ENABLED, "value": True}]]
    await asyncio.sleep(0.05)
    appliance.entities.apply([{"uid": ENABLED, "value": True}])
    await appliance.set_ambient_light(color=(1, 2, 3))
    assert hood.sent[1:] == [[{"uid": CUSTOM, "value": "#010203"}]]


async def test_settings_that_never_appear(
    appliance: Appliance, hood: Hood, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(appliance_module, "AMBIENT_SETTINGS_TIMEOUT", 0.05)
    monkeypatch.setattr(hood, "_lights_on", lambda: None)
    off(appliance, mode=1)
    with pytest.raises(AccessError):
        await appliance.set_ambient_light(color=(255, 0, 0))
    assert hood.sent == [[{"uid": ENABLED, "value": True}]]


async def test_bad_arguments_send_nothing(appliance: Appliance, hood: Hood) -> None:
    appliance.entities.apply([{"uid": ENABLED, "value": True}, {"uid": CUSTOM, "available": True}])
    with pytest.raises(InvalidValueError):
        await appliance.set_ambient_light(color=(1, 2, 3), brightness=50)
    with pytest.raises(InvalidValueError):
        await appliance.set_ambient_light(color=(256, 0, 0))
    assert hood.sent == []
