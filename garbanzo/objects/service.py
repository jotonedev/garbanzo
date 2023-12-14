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
    EXTERNAL = 5


@dataclass
class Service:
    """
    Service object

    :param name: Name of the service
    :param healthchecker: Healthchecker function
    :param interval: Interval in seconds to check the service
    :param service_type: Service type
    :param current_status: Current status of the service
    :param previous_status: Previous statuses of the service
    :param max_previous_status: Max previous statuses to keep (default: 24)
    """
    name: str
    healthchecker: Callable[[], Awaitable[StatusType]]
    interval = 60
    service_type: Optional[ServiceType] = None
    current_status: Status = Status(StatusType.UNKNOWN, int(time.time()))
    previous_status: Deque[Status] = field(default_factory=deque)
    max_previous_status: int = 24

    async def update(self):
        status = await self.healthchecker()

        self.set_status(Status(status=status, time=int(time.time())))

    def set_status(self, status: Status):
        self.previous_status.appendleft(self.current_status)

        if len(self.previous_status) > self.max_previous_status:
            self.previous_status.pop()  # Remove element

        self.current_status = status
