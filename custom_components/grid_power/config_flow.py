from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_DEVICE,
    CONF_INVERT,
    CONF_POLL_INTERVAL,
    DEFAULT_DEVICE,
    DEFAULT_INVERT,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
)
from .device import read_cts


def _schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_DEVICE, default=defaults[CONF_DEVICE]): str,
            vol.Required(
                CONF_POLL_INTERVAL, default=defaults[CONF_POLL_INTERVAL]
            ): vol.All(vol.Coerce(float), vol.Range(min=0.2, max=60)),
            vol.Required(CONF_INVERT, default=defaults[CONF_INVERT]): bool,
        }
    )


class GridPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    read_cts, user_input[CONF_DEVICE], user_input[CONF_INVERT]
                )
            except OSError:
                errors["cannot_connect"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_DEVICE])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Grid power", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=_schema(
                {
                    CONF_DEVICE: DEFAULT_DEVICE,
                    CONF_POLL_INTERVAL: DEFAULT_POLL_INTERVAL,
                    CONF_INVERT: DEFAULT_INVERT,
                }
            ), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return GridPowerOptionsFlow(config_entry)


class GridPowerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        defaults = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(defaults))
