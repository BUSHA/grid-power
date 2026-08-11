from __future__ import annotations

import fcntl
import os

from .const import TIOCMGET, TIOCM_CTS


def read_cts(device: str, invert: bool = False) -> bool:
    """Read the live CTS modem-control bit from a Linux serial device."""
    fd = os.open(device, os.O_RDONLY | os.O_NOCTTY | os.O_NONBLOCK)
    try:
        status = bytearray(4)
        fcntl.ioctl(fd, TIOCMGET, status, True)
        value = bool(int.from_bytes(status, "little") & TIOCM_CTS)
        return not value if invert else value
    finally:
        os.close(fd)
