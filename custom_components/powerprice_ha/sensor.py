"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import const as pp


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""

    config = config_entry.data

    async_add_entities(
        [
            PPSensor(hass, config, name)
            for name in ["price", "price_daily", "price_monthly", "price_yearly"]
        ],
    )


class PPSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, config, postfix):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__()

        self.hass = hass
        self.config = config

        self.energy_id = self.config[pp.CONF_ENERGY_ENTITY_ID]
        self.price_id = self.config[pp.CONF_PRICE_ENTITY_ID]
        self.uid = self.energy_id.removesuffix("_energy") + "_" + postfix

        self._attr_name = self.uid
        self._attr_unique_id = self.uid

        self._attr_native_value = float(
            self.hass.states.get(
                self.energy_id,
            ).state,
        ) * float(
            self.hass.states.get(
                self.price_id,
            ).state,
        )

        async_track_state_change_event(
            self.hass,
            self.energy_id,
            self.async_state_changed_listener_energy,
        )

        async_track_state_change_event(
            self.hass,
            self.price_id,
            self.async_state_changed_listener_price,
        )

    @callback
    def async_state_changed_listener_energy(
        self,
        event: Event[EventStateChangedData] | None = None,
    ) -> None:
        self._attr_native_value = float(event.data["new_state"].state) * float(
            self.hass.states.get(
                self.price_id,
            ).state,
        )
        self.async_write_ha_state()

    @callback
    def async_state_changed_listener_price(
        self,
        event: Event[EventStateChangedData] | None = None,
    ) -> None:
        self._attr_native_value = float(event.data["new_state"].state) * float(
            self.hass.states.get(
                self.energy_id,
            ).state,
        )
        self.async_write_ha_state()
