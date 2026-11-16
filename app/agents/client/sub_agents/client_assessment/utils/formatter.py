import json

from app.domain.constants.tolerance_ranges import TOLERANCE_RANGES


def format_tolerance_ranges() -> str:
    data = {
        behavior.value: {
            "minimum": minimum,
            "maximum": maximum,
        }
        for behavior, (minimum, maximum) in TOLERANCE_RANGES.items()
    }

    return json.dumps(data, ensure_ascii=False, indent=2)
