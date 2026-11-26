import json

from app.domain.constants.tolerance_ranges import TOLERANCE_RANGES
from app.domain.constants.trust_ranges import TRUST_RANGES


def _format_ranges(ranges: dict) -> str:
    data = {
        behavior.value: {
            "minimum": minimum,
            "maximum": maximum,
        }
        for behavior, (minimum, maximum) in ranges.items()
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_tolerance_ranges() -> str:
    return _format_ranges(TOLERANCE_RANGES)


def format_trust_ranges() -> str:
    return _format_ranges(TRUST_RANGES)
