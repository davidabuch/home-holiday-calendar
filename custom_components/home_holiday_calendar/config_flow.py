"""Config flow for Home Holiday Calendar."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import CONF_ISRAEL, DEFAULT_ISRAEL, DOMAIN


class HomeHolidayCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Home Holiday Calendar config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(
                title="Home Holiday Calendar", data=user_input
            )
        schema = vol.Schema(
            {vol.Required(CONF_ISRAEL, default=DEFAULT_ISRAEL): bool}
        )
        return self.async_show_form(step_id="user", data_schema=schema)
