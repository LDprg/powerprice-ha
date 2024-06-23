"""Init for integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Setup up a config entry."""

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            config_entry,
            ["sensor"],
        ),
    )

    return True
