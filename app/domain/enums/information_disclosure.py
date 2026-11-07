
from enum import Enum


class InformationDisclosure(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    VAGUE = "vague"
    ESTIMATED = "estimated"
    DECLINED = "declined"
    UNKNOWN = "unknown"