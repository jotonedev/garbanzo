import time
from enum import Enum
from collections import deque
from dataclasses import dataclass, field

from typing import Callable, Deque, Awaitable, Optional

from .status import StatusType, Status


__all__ = [
    "Service",
    "ServiceType"
]


class ServiceType(Enum):
    TCP = 1
    UDP = 2
    HTTP = 3
    DOCKER = 4


@dataclass
class Service:
    name: str
    healthchecker: Callable[[], Awaitable[StatusType]]
    service_type: Optional[ServiceType] = None
    current_status: Status = Status(StatusType.UNKNOWN, int(time.time()))
    previous_status: Deque[Status] = field(default_factory=deque)

    async def update(self):
        status = await self.healthchecker()

        self.set_status(Status(status=status, time=int(time.time())))

    def set_status(self, status: Status):
        self.previous_status.appendleft(self.current_status)

        if len(self.previous_status) > 24:
            self.previous_status.pop()  # Remove element

        self.current_status = status
