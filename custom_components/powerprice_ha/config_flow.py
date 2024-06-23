"""Config flow"""

from __future__ import annotations

import voluptuous as vol
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.helpers import selector

from . import const as irri


class IrrigationHaFlow(ConfigFlow, domain=irri.DOMAIN):
    """
    config flow
    """

    async def async_step_user(
        self,
        user_input,
    ):
        """
        Init step
        """

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_ENTITY_ID],
                data=user_input,
            )

        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=[
                                SENSOR_DOMAIN,
                            ],
                            multiple=False,
                        ),
                    ),
                },
            ),
        )
