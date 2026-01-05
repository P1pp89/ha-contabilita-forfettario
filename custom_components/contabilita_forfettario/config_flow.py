"""Config flow per Contabilità Forfettario."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ContabilitaForfettarioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow per Contabilità Forfettario."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Gestisce il flusso iniziato dall'utente."""
        if user_input is not None:
            await self.async_set_unique_id("contabilita_forfettario_instance")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title="Contabilità Forfettario",
                data=user_input,
            )

        # Schema per i dati iniziali
        data_schema = vol.Schema({
            vol.Required("anno_inizio_attivita", default=2024): int,
            vol.Required("coefficiente_redditivita", default=0.78): vol.All(
                vol.Coerce(float), vol.Range(min=0, max=1)
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
