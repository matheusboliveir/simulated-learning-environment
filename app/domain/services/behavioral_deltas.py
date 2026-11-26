from dataclasses import dataclass

from app.domain.constants.behavior_weights import BEHAVIOR_WEIGHTS, SECONDARY_FACTOR
from app.domain.constants.tolerance_ranges import (
    TOLERANCE_RANGES,
    TOLERANCE_RECOVERY_FLOOR,
)
from app.domain.constants.trust_ranges import TRUST_DELTA_LIMIT, TRUST_RANGES
from app.domain.enums.behavior_intensity import BehaviorIntensity
from app.domain.enums.behavior_type import BehaviorType

_INTENSITY_ORDER = {
    BehaviorIntensity.LOW: 0,
    BehaviorIntensity.MEDIUM: 1,
    BehaviorIntensity.HIGH: 2,
}


@dataclass(frozen=True)
class BehavioralDeltas:
    trust_delta: float
    tolerance_delta: int


def _value_for_intensity(
    value_range: tuple[float, float],
    intensity: BehaviorIntensity,
) -> float:
    """LOW = extremo mais próximo de zero, MEDIUM = ponto médio,
    HIGH = extremo mais distante de zero."""
    weakest, strongest = sorted(value_range, key=abs)
    if intensity is BehaviorIntensity.LOW:
        return weakest
    if intensity is BehaviorIntensity.HIGH:
        return strongest
    return (weakest + strongest) / 2


def _combine(values: dict[BehaviorType, float]) -> float:
    """Soma com retorno decrescente baseado no peso.

    O comportamento dominante (maior peso; em empate, maior valor absoluto)
    conta 100%. Cada comportamento secundário conta
    SECONDARY_FACTOR x (peso dele / peso do dominante) do seu valor.
    Acrescentar um comportamento nunca inverte o sentido da sua contribuição.
    """
    if not values:
        return 0.0
    ordered = sorted(
        values.items(),
        key=lambda item: (BEHAVIOR_WEIGHTS[item[0]], abs(item[1])),
        reverse=True,
    )
    dominant_behavior, dominant_value = ordered[0]
    dominant_weight = BEHAVIOR_WEIGHTS[dominant_behavior]
    total = dominant_value
    for behavior, value in ordered[1:]:
        factor = SECONDARY_FACTOR * BEHAVIOR_WEIGHTS[behavior] / dominant_weight
        total += factor * value
    return total


def calculate_behavioral_deltas(
    behaviors: list[tuple[BehaviorType, BehaviorIntensity]],
    current_tolerance: float,
    maximum_tolerance: float,
) -> BehavioralDeltas:
    """Calcula as variações de confiança e tolerância de uma mensagem.

    Cada tipo de comportamento conta uma única vez, com a maior intensidade
    informada. A confiança é limitada a ±TRUST_DELTA_LIMIT. Um ganho de
    tolerância é multiplicado pela tolerância atual em relação ao máximo
    (com piso TOLERANCE_RECOVERY_FLOOR); perdas não são reduzidas. A
    tolerância devolvida já é a variação efetiva, depois de limitar o
    resultado entre zero e o máximo do preset.
    """
    strongest: dict[BehaviorType, BehaviorIntensity] = {}
    for behavior, intensity in behaviors:
        previous = strongest.get(behavior)
        if previous is None or _INTENSITY_ORDER[intensity] > _INTENSITY_ORDER[previous]:
            strongest[behavior] = intensity

    raw_trust = _combine(
        {
            behavior: _value_for_intensity(TRUST_RANGES[behavior], intensity)
            for behavior, intensity in strongest.items()
        }
    )
    trust_delta = round(max(-TRUST_DELTA_LIMIT, min(TRUST_DELTA_LIMIT, raw_trust)), 2)

    combined_tolerance = _combine(
        {
            behavior: _value_for_intensity(TOLERANCE_RANGES[behavior], intensity)
            for behavior, intensity in strongest.items()
        }
    )
    if combined_tolerance > 0 and maximum_tolerance > 0:
        # Quem está mais irritado se acalma mais devagar.
        recovery_factor = max(
            TOLERANCE_RECOVERY_FLOOR,
            current_tolerance / maximum_tolerance,
        )
        combined_tolerance *= recovery_factor
    raw_tolerance = round(combined_tolerance)
    tolerance_after = min(maximum_tolerance, max(0, current_tolerance + raw_tolerance))
    tolerance_delta = int(round(tolerance_after - current_tolerance))

    return BehavioralDeltas(trust_delta=trust_delta, tolerance_delta=tolerance_delta)
