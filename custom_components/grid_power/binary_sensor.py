from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GridPowerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GridPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([GridPowerSensor(coordinator, entry)])


class GridPowerSensor(CoordinatorEntity[GridPowerCoordinator], BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER
    _attr_name = "Grid power"
    _attr_has_entity_name = True

    def __init__(self, coordinator: GridPowerCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_grid_power"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Grid power detector",
            "manufacturer": "Local USB sensor",
            "model": "FT232 CTS mains detector",
        }

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data
