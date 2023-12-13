from enum import Enum
from dataclasses import dataclass


__all__ = [
    "Status",
    "StatusType"
]


class StatusType(Enum):
    SUCCESSFUL = 0
    WARNING = 1
    FAILURE = 2
    UNKNOWN = 4


@dataclass(frozen=True)
class Status:
    status: StatusType
    time: int
