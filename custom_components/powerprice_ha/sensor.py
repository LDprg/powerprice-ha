"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_ENTITY_ID

from . import const as irri

async def async_setup_entry(
    _hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""

    config = config_entry.data

    async_add_entities(
        [IRRISensor(config[CONF_ENTITY_ID], name) for name in ["price", "price_daily", "price_monthly", "price_yearly"]],
    )


class IRRISensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, entity_id, postfix):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__()
        
        self.entity_id = entity_id
        self.uid = self.entity_id.removesuffix("_energy") + "_" + postfix

        self._attr_name = self.uid
        self._attr_unique_id = self.uid

