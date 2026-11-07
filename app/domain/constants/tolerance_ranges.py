from typing import Final

from app.domain.enums.behavior_type import BehaviorType

TOLERANCE_RANGES: Final = {
    BehaviorType.REPETITIVE_QUESTION: (-5, -2),
    BehaviorType.OFF_TOPIC_QUESTION: (-8, -2),
    BehaviorType.JAILBREAK_ATTEMPT: (-10, -5),
    BehaviorType.CONFUSING_QUESTION: (-3, -1),
    BehaviorType.INVASIVE_QUESTION: (-8, -3),
    BehaviorType.OFFENSIVE_COMMENT: (-15, -8),
    BehaviorType.ACTIVE_LISTENING: (1, 3),
    BehaviorType.RELEVANT_QUESTION: (1, 2),
    BehaviorType.VIABLE_SOLUTION: (3, 10),
    BehaviorType.FRIENDLINESS: (1, 2),
}