from __future__ import annotations

DOMAIN = "grid_power"
CONF_DEVICE = "device"
CONF_POLL_INTERVAL = "poll_interval"
CONF_INVERT = "invert"

DEFAULT_DEVICE = "/dev/ttyUSB1"
DEFAULT_POLL_INTERVAL = 1.0
DEFAULT_INVERT = False

TIOCMGET = 0x5415
TIOCM_CTS = 0x20
