"""Piattaforma Number per Contabilità Forfettario."""
import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up dei number entities."""
    
    entities = [
        ContabilitaNumber(
            "anno_inizio_attivita",
            "Contabilità Forfettario Anno Inizio Attività",
            2000,
            2100,
            1,
            None,
            config_entry.data.get("anno_inizio_attivita", 2024),
        ),
        ContabilitaNumber(
            "coefficiente_redditivita",
            "Contabilità Forfettario Coefficiente Redditività",
            0,
            1,
            0.01,
            None,
            config_entry.data.get("coefficiente_redditivita", 0.78),
        ),
        ContabilitaNumber(
            "contributi_inps_anno_precedente",
            "Contabilità Forfettario Contributi INPS Anno Precedente",
            0,
            100000,
            1,
            "€",
            0,
        ),
        ContabilitaNumber(
            "ricavi_annui",
            "Contabilità Forfettario Ricavi Annui",
            0,
            85000,
            100,
            "€",
            0,
        ),
        ContabilitaNumber(
            "imposta_netta_anno_precedente",
            "Contabilità Forfettario Imposta Netta Anno Precedente",
            0,
            50000,
            10,
            "€",
            0,
        ),
    ]
    
    async_add_entities(entities)


class ContabilitaNumber(NumberEntity, RestoreEntity):
    """Rappresenta un input number per la contabilità."""

    def __init__(
        self,
        unique_id: str,
        name: str,
        min_value: float,
        max_value: float,
        step: float,
        unit: str | None,
        default_value: float,
    ):
        """Inizializza il number entity."""
        self._attr_unique_id = f"{DOMAIN}_{unique_id}"
        self._attr_name = name
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._attr_mode = NumberMode.BOX
        self._attr_native_value = default_value
        self._attr_has_entity_name = False

    async def async_added_to_hass(self):
        """Ripristina lo stato precedente."""
        await super().async_added_to_hass()
        
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state not in (None, "unknown", "unavailable"):
                try:
                    self._attr_native_value = float(last_state.state)
                except (ValueError, TypeError):
                    pass

    async def async_set_native_value(self, value: float) -> None:
        """Aggiorna il valore."""
        self._attr_native_value = value
        self.async_write_ha_state()
