from typing import Final

from app.domain.enums.behavior_type import BehaviorType

# Variação de tolerância por comportamento (mínimo, máximo), em pontos.
# Faixas negativas são maiores que as positivas (assimetria negativa:
# Baumeister et al., 2001; Slovic, 1993). Os valores de uma mensagem são
# combinados por peso em behavioral_deltas.py. Calibração: duas interações
# ofensivas de intensidade média levam um preset profissional (100) a ~40.
TOLERANCE_RANGES: Final = {
    BehaviorType.REPETITIVE_QUESTION: (-12, -5),
    BehaviorType.OFF_TOPIC_QUESTION: (-20, -8),
    BehaviorType.JAILBREAK_ATTEMPT: (-25, -12),
    BehaviorType.CONFUSING_QUESTION: (-10, -3),
    BehaviorType.INVASIVE_QUESTION: (-20, -8),
    BehaviorType.OFFENSIVE_COMMENT: (-35, -25),
    BehaviorType.BELIEF_CHALLENGE: (-15, -5),
    BehaviorType.ACTIVE_LISTENING: (5, 12),
    BehaviorType.RELEVANT_QUESTION: (3, 10),
    BehaviorType.VIABLE_SOLUTION: (8, 15),
    BehaviorType.FRIENDLINESS: (3, 8),
}

# Ganhos de tolerância são multiplicados pela tolerância atual em relação ao
# máximo do preset (quem está mais irritado se acalma mais devagar), nunca
# abaixo deste piso.
TOLERANCE_RECOVERY_FLOOR: Final = 0.25
