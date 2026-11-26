from typing import Final

from app.domain.enums.behavior_type import BehaviorType

# Variação máxima de confiança em uma única interação, para mais ou para menos.
TRUST_DELTA_LIMIT: Final = 0.30

# Variação de confiança por comportamento (mínimo, máximo), na escala de 1 a 5.
# Calibração (com a combinação por peso de behavioral_deltas.py): uma
# interação "bem positiva" (escuta ativa + pergunta relevante + cordialidade,
# intensidade média) soma ~0,24; seis delas levam a confiança de 1,0 para ~2,5.
# Faixas negativas são maiores que as positivas (Slovic, 1993; Baumeister et
# al., 2001).
TRUST_RANGES: Final = {
    BehaviorType.REPETITIVE_QUESTION: (-0.06, 0.0),
    BehaviorType.OFF_TOPIC_QUESTION: (-0.08, -0.02),
    BehaviorType.JAILBREAK_ATTEMPT: (-0.22, -0.12),
    BehaviorType.CONFUSING_QUESTION: (-0.08, -0.02),
    BehaviorType.INVASIVE_QUESTION: (-0.20, -0.08),
    BehaviorType.OFFENSIVE_COMMENT: (-0.30, -0.22),
    BehaviorType.BELIEF_CHALLENGE: (-0.10, -0.02),
    BehaviorType.ACTIVE_LISTENING: (0.12, 0.24),
    BehaviorType.RELEVANT_QUESTION: (0.08, 0.20),
    BehaviorType.VIABLE_SOLUTION: (0.10, 0.25),
    BehaviorType.FRIENDLINESS: (0.04, 0.12),
}
