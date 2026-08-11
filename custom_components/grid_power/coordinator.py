from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_DEVICE, CONF_INVERT, CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
from .device import read_cts

_LOGGER = logging.getLogger(__name__)


class GridPowerCoordinator(DataUpdateCoordinator[bool]):
    """Poll CTS without blocking Home Assistant's event loop."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        self.device = config[CONF_DEVICE]
        self.invert = config.get(CONF_INVERT, False)
        interval = float(config.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL))
        super().__init__(
            hass,
            _LOGGER,
            name="grid_power",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self) -> bool:
        try:
            return await self.hass.async_add_executor_job(
                read_cts, self.device, self.invert
            )
        except OSError as err:
            raise UpdateFailed(f"Cannot read CTS from {self.device}: {err}") from err
