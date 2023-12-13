import ipaddress
import re

__all__ = [
    "check_domain",
    "check_ip_address"
]


def check_domain(s):
    if re.match(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", s, re.IGNORECASE):
        return "Domain"
    else:
        return "Neither"


def check_ip_address(s):
    try:
        ipaddress.ip_address(s)
        return "IP"
    except ValueError:
        pass
