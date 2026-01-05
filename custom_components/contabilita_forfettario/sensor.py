"""Piattaforma Sensor per Contabilità Forfettario."""
import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    DOMAIN,
    ALIQUOTA_STARTUP,
    ALIQUOTA_ORDINARIA,
    ANNI_ALIQUOTA_AGEVOLATA,
    ALIQUOTA_INPS,
    SOGLIA_ACCONTO_MINIMO,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up dei sensor entities."""
    
    entities = [
        # Sensori base
        RicaviAnnuiSensor(),
        RedditoForfettarioSensor(),
        ContributiINPSSensor(),
        AliquotaImpostaForfettarioSensor(),
        BaseImponibileImpostaSensor(),
        ImpostaSostitutivaSensor(),
        CaricoFiscaleRealeSensor(),
        UtileNettoStimatoSensor(),
        
        # Sensori anno precedente
        RicaviAnnoPrecedenteSensor(),
        RedditoForfettarioAnnoPrecedenteSensor(),
        BaseImponibileAnnoPrecedenteSensor(),
        ImpostaNettaAnnoPrecedenteSensor(),
        
        # Acconti
        AccontoTotaleImpostaSensor(),
        AccontoGiugnoSensor(),
        AccontoNovembreSensor(),
    ]
    
    async_add_entities(entities)


class ContabilitaBaseSensor(SensorEntity):
    """Classe base per i sensori di contabilità."""

    def __init__(self, unique_id: str, name: str, unit: str | None = None):
        """Inizializza il sensore."""
        self._attr_unique_id = f"{DOMAIN}_{unique_id}"
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_should_poll = False

    async def async_added_to_hass(self):
        """Quando l'entità viene aggiunta a HA."""
        await super().async_added_to_hass()
        
        # Traccia i cambiamenti delle entità da cui dipendiamo
        dependencies = self.get_dependencies()
        if dependencies:
            @callback
            def state_changed_listener(event):
                """Aggiorna quando cambiano le dipendenze."""
                self.async_schedule_update_ha_state(True)
            
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, dependencies, state_changed_listener
                )
            )
        
        # Aggiorna subito
        self.async_schedule_update_ha_state(True)

    def get_dependencies(self) -> list[str]:
        """Ritorna la lista delle entità da cui dipende questo sensore."""
        return []

    def get_state_value(self, entity_id: str, default: float = 0.0) -> float:
        """Helper per ottenere il valore di un'entità."""
        state = self.hass.states.get(entity_id)
        if state is None or state.state in ("unknown", "unavailable", ""):
            return default
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return default


class RicaviAnnuiSensor(ContabilitaBaseSensor):
    """Sensore per ricavi annui."""

    def __init__(self):
        super().__init__("ricavi_annui_2", "Ricavi Annui", "€")
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def get_dependencies(self) -> list[str]:
        return [f"number.{DOMAIN}_ricavi_annui"]

    @property
    def native_value(self):
        return self.get_state_value(f"number.{DOMAIN}_ricavi_annui")


class RedditoForfettarioSensor(ContabilitaBaseSensor):
    """Sensore per reddito forfettario."""

    def __init__(self):
        super().__init__("reddito_forfettario", "Reddito Forfettario", "€")
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def get_dependencies(self) -> list[str]:
        return [
            f"number.{DOMAIN}_ricavi_annui",
            f"number.{DOMAIN}_coefficiente_redditivita",
        ]

    @property
    def native_value(self):
        ricavi = self.get_state_value(f"number.{DOMAIN}_ricavi_annui")
        coeff = self.get_state_value(f"number.{DOMAIN}_coefficiente_redditivita", 0.78)
        return round(ricavi * coeff, 2)


class ContributiINPSSensor(ContabilitaBaseSensor):
    """Sensore per contributi INPS."""

    def __init__(self):
        super().__init__("contributi_inps", "Contributi INPS", "€")

    def get_dependencies(self) -> list[str]:
        return [f"sensor.{DOMAIN}_reddito_forfettario"]

    @property
    def native_value(self):
        reddito = self.get_state_value(f"sensor.{DOMAIN}_reddito_forfettario")
        return round(reddito * ALIQUOTA_INPS, 2)


class AliquotaImpostaForfettarioSensor(ContabilitaBaseSensor):
    """Sensore per aliquota imposta forfettario."""

    def __init__(self):
        super().__init__("aliquota_imposta_forfettario", "Aliquota Imposta Forfettario", "%")

    def get_dependencies(self) -> list[str]:
        return [f"number.{DOMAIN}_anno_inizio_attivita"]

    @property
    def native_value(self):
        anno_corrente = datetime.now().year
        anno_start = int(self.get_state_value(f"number.{DOMAIN}_anno_inizio_attivita", anno_corrente))
        
        if (anno_corrente - anno_start) < ANNI_ALIQUOTA_AGEVOLATA:
            return ALIQUOTA_STARTUP
        return ALIQUOTA_ORDINARIA


class BaseImponibileImpostaSensor(ContabilitaBaseSensor):
    """Sensore per base imponibile imposta."""

    def __init__(self):
        super().__init__("base_imponibile_imposta", "Base Imponibile Imposta", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_reddito_forfettario",
            f"sensor.{DOMAIN}_contributi_inps",
        ]

    @property
    def native_value(self):
        reddito = self.get_state_value(f"sensor.{DOMAIN}_reddito_forfettario")
        inps = self.get_state_value(f"sensor.{DOMAIN}_contributi_inps")
        return round(reddito - inps, 2)


class ImpostaSostitutivaSensor(ContabilitaBaseSensor):
    """Sensore per imposta sostitutiva."""

    def __init__(self):
        super().__init__("imposta_sostitutiva", "Imposta Sostitutiva", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_base_imponibile_imposta",
            f"sensor.{DOMAIN}_aliquota_imposta_forfettario",
        ]

    @property
    def native_value(self):
        base = self.get_state_value(f"sensor.{DOMAIN}_base_imponibile_imposta")
        aliquota = self.get_state_value(f"sensor.{DOMAIN}_aliquota_imposta_forfettario")
        return round(base * (aliquota / 100), 2)


class CaricoFiscaleRealeSensor(ContabilitaBaseSensor):
    """Sensore per carico fiscale reale."""

    def __init__(self):
        super().__init__("carico_fiscale_reale", "Carico Fiscale Reale", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_contributi_inps",
            f"sensor.{DOMAIN}_imposta_sostitutiva",
        ]

    @property
    def native_value(self):
        inps = self.get_state_value(f"sensor.{DOMAIN}_contributi_inps")
        imposta = self.get_state_value(f"sensor.{DOMAIN}_imposta_sostitutiva")
        return round(inps + imposta, 2)


class UtileNettoStimatoSensor(ContabilitaBaseSensor):
    """Sensore per utile netto stimato."""

    def __init__(self):
        super().__init__("utile_netto_stimato", "Utile Netto Stimato", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"number.{DOMAIN}_ricavi_annui",
            f"sensor.{DOMAIN}_carico_fiscale_reale",
        ]

    @property
    def native_value(self):
        ricavi = self.get_state_value(f"number.{DOMAIN}_ricavi_annui")
        carico = self.get_state_value(f"sensor.{DOMAIN}_carico_fiscale_reale")
        return round(ricavi - carico, 2)


class RicaviAnnoPrecedenteSensor(ContabilitaBaseSensor):
    """Sensore per ricavi anno precedente (dal utility meter)."""

    def __init__(self):
        super().__init__("ricavi_anno_precedente", "Ricavi Anno Precedente", "€")

    def get_dependencies(self) -> list[str]:
        return [f"sensor.{DOMAIN}_ricavi_annui_last_year"]

    @property
    def native_value(self):
        # Questo dipende dal utility_meter che va configurato separatamente
        return self.get_state_value(f"sensor.{DOMAIN}_ricavi_annui_last_year")


class RedditoForfettarioAnnoPrecedenteSensor(ContabilitaBaseSensor):
    """Sensore per reddito forfettario anno precedente."""

    def __init__(self):
        super().__init__("reddito_forfettario_anno_precedente", "Reddito Forfettario Anno Precedente", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_ricavi_anno_precedente",
            f"number.{DOMAIN}_coefficiente_redditivita",
        ]

    @property
    def native_value(self):
        ricavi = self.get_state_value(f"sensor.{DOMAIN}_ricavi_anno_precedente")
        coeff = self.get_state_value(f"number.{DOMAIN}_coefficiente_redditivita", 0.78)
        return round(ricavi * coeff, 2)


class BaseImponibileAnnoPrecedenteSensor(ContabilitaBaseSensor):
    """Sensore per base imponibile anno precedente."""

    def __init__(self):
        super().__init__("base_imponibile_anno_precedente", "Base Imponibile Anno Precedente", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_reddito_forfettario_anno_precedente",
            f"number.{DOMAIN}_contributi_inps_anno_precedente",
        ]

    @property
    def native_value(self):
        reddito = self.get_state_value(f"sensor.{DOMAIN}_reddito_forfettario_anno_precedente")
        inps = self.get_state_value(f"number.{DOMAIN}_contributi_inps_anno_precedente")
        base = reddito - inps
        return round(max(base, 0), 2)


class ImpostaNettaAnnoPrecedenteSensor(ContabilitaBaseSensor):
    """Sensore per imposta netta anno precedente."""

    def __init__(self):
        super().__init__("imposta_netta_anno_precedente", "Imposta Netta Anno Precedente", "€")

    def get_dependencies(self) -> list[str]:
        return [
            f"sensor.{DOMAIN}_base_imponibile_anno_precedente",
            f"number.{DOMAIN}_anno_inizio_attivita",
        ]

    @property
    def native_value(self):
        base = self.get_state_value(f"sensor.{DOMAIN}_base_imponibile_anno_precedente")
        if base <= 0:
            return 0
        
        anno_corrente = datetime.now().year
        anno_start = int(self.get_state_value(f"number.{DOMAIN}_anno_inizio_attivita", anno_corrente))
        
        # Anno precedente
        if (anno_corrente - anno_start - 1) < ANNI_ALIQUOTA_AGEVOLATA:
            aliquota = ALIQUOTA_STARTUP
        else:
            aliquota = ALIQUOTA_ORDINARIA
        
        return round(base * (aliquota / 100), 2)


class AccontoTotaleImpostaSensor(ContabilitaBaseSensor):
    """Sensore per acconto totale imposta."""

    def __init__(self):
        super().__init__("acconto_totale_imposta", "Acconto Totale Imposta", "€")

    def get_dependencies(self) -> list[str]:
        return [f"sensor.{DOMAIN}_imposta_netta_anno_precedente"]

    @property
    def native_value(self):
        imp = self.get_state_value(f"sensor.{DOMAIN}_imposta_netta_anno_precedente")
        if imp < SOGLIA_ACCONTO_MINIMO:
            return 0
        return round(imp, 2)


class AccontoGiugnoSensor(ContabilitaBaseSensor):
    """Sensore per acconto giugno."""

    def __init__(self):
        super().__init__("acconto_giugno", "Acconto Giugno", "€")

    def get_dependencies(self) -> list[str]:
        return [f"sensor.{DOMAIN}_acconto_totale_imposta"]

    @property
    def native_value(self):
        totale = self.get_state_value(f"sensor.{DOMAIN}_acconto_totale_imposta")
        return round(totale * 0.5, 2)


class AccontoNovembreSensor(ContabilitaBaseSensor):
    """Sensore per acconto novembre."""

    def __init__(self):
        super().__init__("acconto_novembre", "Acconto Novembre", "€")

    def get_dependencies(self) -> list[str]:
        return [f"sensor.{DOMAIN}_acconto_totale_imposta"]

    @property
    def native_value(self):
        totale = self.get_state_value(f"sensor.{DOMAIN}_acconto_totale_imposta")
        return round(totale * 0.5, 2)
