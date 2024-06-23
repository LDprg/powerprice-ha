"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event, EventStateChangedData, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)

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
            for name in ["", "_daily", "_monthly", "_yearly"]
        ],
    )


class PPSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, config, suffix):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__()

        self.hass = hass
        self.config = config

        self.energy_id = self.config[pp.CONF_ENERGY_ENTITY_ID] + suffix
        self.price_id = self.config[pp.CONF_PRICE_ENTITY_ID]
        self.uid = self.energy_id.removesuffix("_energy" + suffix) + "_price" + suffix

        self._attr_name = self.uid
        self._attr_unique_id = self.uid

        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "€"

        energy = self.hass.states.get(self.energy_id)
        price = self.hass.states.get(self.price_id)
        if (
            energy is not None
            and price is not None
            and energy.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
            and price.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
        ):
            self._attr_native_value = float(energy.state) * float(price.state)

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
        energy = event.data["new_state"]
        price = self.hass.states.get(self.price_id)
        if (
            energy is not None
            and price is not None
            and energy.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
            and price.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
        ):
            self._attr_native_value = float(energy.state) * float(price.state)
        self.async_write_ha_state()

    @callback
    def async_state_changed_listener_price(
        self,
        event: Event[EventStateChangedData] | None = None,
    ) -> None:
        energy = self.hass.states.get(self.energy_id)
        price = event.data["new_state"]
        if (
            energy is not None
            and price is not None
            and energy.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
            and price.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE)
        ):
            self._attr_native_value = float(energy.state) * float(price.state)
        self.async_write_ha_state()
