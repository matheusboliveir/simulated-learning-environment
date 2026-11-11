import json

from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES
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


def format_tolerance_initial_values() -> str:
    data = {
        behavior.value: value for behavior, value in TOLERANCE_INITIAL_VALUES.items()
    }

    return json.dumps(data, ensure_ascii=False, indent=2)
