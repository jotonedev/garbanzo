import asyncio
import logging

from socket import AF_INET, AddressFamily
from aiodns import DNSResolver
from typing import Callable, Awaitable, Optional

from ..objects.status import StatusType
from ..utils import check_domain, check_ip_address


def tcp_builder(
        host: str,
        port: int,
        payload: bytes,
        response: bytes,
        timeout: int = 5,
        fail_on_timeout: bool = False,
        fail_on_wrong_response: bool = False,
        ssl: bool = False,
        socket_family: AddressFamily = AF_INET,
        dns_resolver: Optional[DNSResolver] = None
) -> Callable[[], Awaitable[StatusType]]:
    # Create logger with the host name
    logger = logging.getLogger(f"tcp.{host.replace('.', '-')}")

    # check if a domain name is provided and if a DNSResolver is provided
    # if not, create a new DNSResolver
    if dns_resolver is None and check_domain(host):
        loop = asyncio.get_event_loop()
        dns_resolver = DNSResolver(loop=loop)

    # if the host is an ip address, we can use it directly
    if check_ip_address(host):
        address = host
    else:
        address = None

    async def tcp_healthcheck() -> StatusType:
        # noinspection PyGlobalUndefined
        global address

        # Because the ip address can change overtime, we need to resolve the domain name every time
        if address is None:
            address = await dns_resolver.gethostbyname(host, socket_family)
            server_hostname = host if ssl else None  # If ssl is enabled and the host is a domain name, we can use SNI
        else:
            server_hostname = None

        # noinspection PyBroadException
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port, ssl=ssl, server_hostname=server_hostname),
                timeout=timeout
            )
            writer.write(payload)

            await writer.drain()
            data = await reader.read(100)
            writer.close()
            await writer.wait_closed()

            if data == response:
                return StatusType.SUCCESSFUL
            else:
                if fail_on_wrong_response:
                    return StatusType.FAILURE
                else:
                    return StatusType.WARNING
        except asyncio.TimeoutError:
            if fail_on_timeout:
                return StatusType.FAILURE
            else:
                return StatusType.WARNING
        except Exception as e:
            logger.info(f"Connection failed to {host}:{port}, error: {e}")
            return StatusType.FAILURE

    return tcp_healthcheck
