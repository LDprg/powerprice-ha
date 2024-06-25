"""Config flow"""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.input_number import DOMAIN as INPUT_NUMBER_DOMAIN
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.helpers import selector
from homeassistant.core import callback

from . import const as pp


class PowerPriceHaFlow(ConfigFlow, domain=pp.DOMAIN):
    """
    config flow
    """

    async def async_step_init(self, user_input):
        """
        Init step
        """

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[pp.CONF_ENERGY_ENTITY_ID],
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
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

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input,
    ):
        """Manage the options."""
        self.current_config = dict(self.config_entry.data)

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        pp.CONF_ENERGY_ENTITY_ID,
                        default=self.current_config.get(pp.CONF_ENERGY_ENTITY_ID),
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
                        default=self.current_config.get(pp.CONF_PRICE_ENTITY_ID),
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
