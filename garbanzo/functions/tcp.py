import anyio
import logging

from typing import Callable, Awaitable, Optional

from ..objects.status import StatusType


def tcp_builder(
        host: str,
        port: int,
        payload: bytes,
        response: bytes,
        timeout: int = 5,
        fail_on_timeout: bool = False,
        fail_on_wrong_response: bool = False,
        ssl: bool = False,
) -> Callable[[], Awaitable[StatusType]]:
    # Create logger with the host name
    logger = logging.getLogger(f"tcp.{host.replace('.', '-')}")

    async def tcp_healthcheck() -> StatusType:
        # noinspection PyBroadException
        try:
            async with anyio.fail_after(timeout):
                # noinspection PyTypeChecker
                async with await anyio.connect_tcp(remote_host=host, remote_port=port, tls=ssl) as stream:
                    await stream.send(payload)
                    data = await stream.receive()

                    if data == response:
                        return StatusType.SUCCESSFUL
                    else:
                        if fail_on_wrong_response:
                            return StatusType.FAILURE
                        else:
                            return StatusType.WARNING
        except TimeoutError:
            if fail_on_timeout:
                return StatusType.FAILURE
            else:
                return StatusType.WARNING
        except Exception as e:
            logger.info(f"Connection failed to {host}:{port}, error: {e}")
            return StatusType.FAILURE

    return tcp_healthcheck
