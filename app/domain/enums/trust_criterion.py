from enum import Enum


class TrustCriterion(str, Enum):
    STRUCTURED_COMMUNICATION = "structured_communication"
    COMMUNICATIONAL_COHERENCE = "communicational_coherence"
    LANGUAGE_APPROPRIATENESS = "language_appropriateness"
    QUESTION_CLARITY = "question_clarity"
    ACTIVE_LISTENING = "active_listening"
    PROACTIVITY = "proactivity"
    PROFESSIONALISM = "professionalism"
    CHARISMA = "charisma"
    RESPECT = "respect"