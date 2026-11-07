from enum import Enum


class BehaviorType(str, Enum):
    REPETITIVE_QUESTION = "repetitive_question"
    OFF_TOPIC_QUESTION = "off_topic_question"
    JAILBREAK_ATTEMPT = "jailbreak_attempt"
    CONFUSING_QUESTION = "confusing_question"
    INVASIVE_QUESTION = "invasive_question"
    OFFENSIVE_COMMENT = "offensive_comment"
    ACTIVE_LISTENING = "active_listening"
    RELEVANT_QUESTION = "relevant_question"
    VIABLE_SOLUTION = "viable_solution"
    FRIENDLINESS = "friendliness"