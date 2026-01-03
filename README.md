# Home Assistant Partita IVA

📊 Package per la gestione contabile di Partita IVA in Home Assistant.  

Gestisce automaticamente:  
- Calcolo reddito forfettario  
- Contributi INPS  
- Imposta sostitutiva secondo aliquota attuale (5% primi 5 anni, 15% dopo)  
- Utile netto stimato  
- Utility Meter per ricavi annui e anno precedente  

---

## Installazione

### Con HACS (consigliato)

1. Vai in **HACS → Custom repositories**  
2. Inserisci l’URL del repository: `https://github.com/P1pp89/ha-contabilita-forfettario 
3. Tipo: **Integration**  
4. Installa il package direttamente da HACS  
5. Riavvia Home Assistant

### Manuale

1. Copia la cartella `packages/` nel tuo percorso `homeassistant/` di Home Assistant  
2. Aggiungi al `configuration.yaml` se non presente:

le righe:

homeassistant:
  packages: !include_dir_named packages

3. Riavvia Home Assistant
