from typing import Final

from app.domain.enums.tolerance_preset import TolerancePreset

TOLERANCE_INITIAL_VALUES: Final = {
    TolerancePreset.INTOLERANT: 60,
    TolerancePreset.IMPATIENT: 75,
    TolerancePreset.PROFESSIONAL: 100,
    TolerancePreset.SOCIABLE: 110,
    TolerancePreset.UNDERSTANDING: 120,
}