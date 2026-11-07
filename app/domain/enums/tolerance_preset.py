from enum import Enum


class TolerancePreset(str, Enum):
    INTOLERANT = "intolerant"
    IMPATIENT = "impatient"
    PROFESSIONAL = "professional"
    SOCIABLE = "sociable"
    UNDERSTANDING = "understanding"