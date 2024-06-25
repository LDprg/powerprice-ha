"""Config flow"""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.input_number import DOMAIN as INPUT_NUMBER_DOMAIN
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import selector

from . import const as pp


class PowerPriceHaFlow(ConfigFlow, domain=pp.DOMAIN):
    """
    config flow
    """

    async def async_step_user(self, user_input):
        """
        Init step
        """

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[pp.CONF_ENERGY_ENTITY_ID],
                data=user_input,
            )

        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    vol.Required(pp.CONF_ENERGY_ENTITY_ID): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=[
                                SENSOR_DOMAIN,
                            ],
                            multiple=False,
                        ),
                    ),
                    vol.Required(pp.CONF_PRICE_ENTITY_ID): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=[
                                SENSOR_DOMAIN,
                                INPUT_NUMBER_DOMAIN,
                            ],
                            multiple=False,
                        ),
                    ),
                },
            ),
        )

    async def async_step_reconfigure(
        self,
        user_input,
    ):
        """Handle a reconfiguration flow initialized by the user."""

        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])

        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                reason="reconfigure_successful",
                data=user_input,
            )

        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    vol.Required(
                        pp.CONF_ENERGY_ENTITY_ID,
                        default=entry.data.get(pp.CONF_ENERGY_ENTITY_ID),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=[
                                SENSOR_DOMAIN,
                            ],
                            multiple=False,
                        ),
                    ),
                    vol.Required(
                        pp.CONF_PRICE_ENTITY_ID,
                        default=entry.data.get(pp.CONF_PRICE_ENTITY_ID),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=[
                                SENSOR_DOMAIN,
                                INPUT_NUMBER_DOMAIN,
                            ],
                            multiple=False,
                        ),
                    ),
                },
            ),
        )
