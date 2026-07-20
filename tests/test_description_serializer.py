from __future__ import annotations

import json
from pathlib import Path

import pytest
from home_disconnect.description_parser import parse_device_description
from home_disconnect.description_serializer import serialize_device_description


@pytest.mark.parametrize(
    ("description_path", "feature_path"),
    [
        (Path("tests/DeviceDescription.xml"), Path("tests/FeatureMapping.xml")),
        (
            Path("tests/DeviceDescription_short.xml"),
            Path("tests/FeatureMapping_short.xml"),
        ),
    ],
)
def test_serialize_device_description_round_trip(
    description_path: Path, feature_path: Path
) -> None:
    """Serializing then re-parsing a description must produce the same result."""
    with description_path.open() as file:
        description_file = file.read()
    with feature_path.open() as file:
        feature_file = file.read()

    original = parse_device_description(description_file, feature_file)

    new_description_xml, new_feature_xml = serialize_device_description(original)
    round_tripped = parse_device_description(new_description_xml, new_feature_xml)

    # Normalize through JSON the same way test_description_parser.py does, since
    # dict keys (e.g. enumeration value -> name) become strings either way.
    original = json.loads(json.dumps(original))
    round_tripped = json.loads(json.dumps(round_tripped))

    assert round_tripped == original
