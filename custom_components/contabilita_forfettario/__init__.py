"""Integrazione Contabilità Forfettario per Home Assistant."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "contabilita_forfettario"
PLATFORMS = ["sensor", "number"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up del componente via configuration.yaml."""
    # Non facciamo nulla qui, tutto viene gestito dal config_entry
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up da config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Setup delle piattaforme
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    
    return unload_ok
