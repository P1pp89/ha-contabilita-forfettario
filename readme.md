# Contabilità Forfettario per Home Assistant

Integrazione per gestire la contabilità del regime forfettario italiano direttamente in Home Assistant.

## Caratteristiche

✅ Calcolo automatico del reddito forfettario  
✅ Calcolo contributi INPS  
✅ Calcolo imposta sostitutiva con aliquote agevolate (5% primi 5 anni)  
✅ Calcolo acconti fiscali (giugno e novembre)  
✅ Stima dell'utile netto  
✅ Tracking ricavi annuali  

## Installazione

### Via HACS (Consigliato)

1. Aggiungi questo repository a HACS come repository personalizzato
2. Cerca "Contabilità Forfettario" in HACS
3. Clicca "Install"
4. Riavvia Home Assistant
5. Vai in **Impostazioni** → **Dispositivi e Servizi** → **Aggiungi Integrazione**
6. Cerca "Contabilità Forfettario"

### Manuale

1. Copia la cartella `custom_components/contabilita_forfettario` nella tua cartella `custom_components` di Home Assistant
2. Riavvia Home Assistant
3. Vai in **Impostazioni** → **Dispositivi e Servizi** → **Aggiungi Integrazione**
4. Cerca "Contabilità Forfettario"

## Configurazione

Durante l'installazione ti verrà chiesto di inserire:

- **Anno Inizio Attività**: L'anno in cui hai aperto la partita IVA (per calcolare l'aliquota agevolata)
- **Coefficiente Redditività**: Il coefficiente del tuo codice ATECO (default 78% = 0.78)

## Entità Create

### Input Number (Valori da Inserire)

- `number.contabilita_forfettario_anno_inizio_attivita` - Anno inizio attività
- `number.contabilita_forfettario_coefficiente_redditivita` - Coefficiente redditività
- `number.contabilita_forfettario_contributi_inps_anno_precedente` - Contributi INPS pagati l'anno scorso
- `number.contabilita_forfettario_ricavi_annui` - Ricavi annui stimati
- `number.contabilita_forfettario_imposta_netta_anno_precedente` - Imposta netta anno precedente

### Sensori Calcolati

#### Calcoli Correnti
- `sensor.contabilita_forfettario_ricavi_annui_2` - Ricavi annui (per utility meter)
- `sensor.contabilita_forfettario_reddito_forfettario` - Reddito forfettario calcolato
- `sensor.contabilita_forfettario_contributi_inps` - Contributi INPS da pagare
- `sensor.contabilita_forfettario_aliquota_imposta_forfettario` - Aliquota applicata (5% o 15%)
- `sensor.contabilita_forfettario_base_imponibile_imposta` - Base imponibile
- `sensor.contabilita_forfettario_imposta_sostitutiva` - Imposta sostitutiva
- `sensor.contabilita_forfettario_carico_fiscale_reale` - Totale tasse da pagare
- `sensor.contabilita_forfettario_utile_netto_stimato` - Utile netto stimato

#### Anno Precedente
- `sensor.contabilita_forfettario_ricavi_anno_precedente` - Ricavi anno scorso
- `sensor.contabilita_forfettario_reddito_forfettario_anno_precedente` - Reddito forfettario anno scorso
- `sensor.contabilita_forfettario_base_imponibile_anno_precedente` - Base imponibile anno scorso
- `sensor.contabilita_forfettario_imposta_netta_anno_precedente` - Imposta netta anno scorso

#### Acconti
- `sensor.contabilita_forfettario_acconto_totale_imposta` - Acconto totale da pagare
- `sensor.contabilita_forfettario_acconto_giugno` - Acconto di giugno
- `sensor.contabilita_forfettario_acconto_novembre` - Acconto di novembre

## Utility Meter

Per tracciare i ricavi anno per anno, aggiungi al tuo `configuration.yaml`:

```yaml
utility_meter:
  contabilita_forfettario_ricavi_annui:
    source: sensor.contabilita_forfettario_ricavi_annui_2
    cycle: yearly
```

Questo creerà automaticamente:
- `sensor.contabilita_forfettario_ricavi_annui_last_year` - Ricavi dell'anno precedente

## Esempio Dashboard

```yaml
type: entities
title: Contabilità Forfettario
entities:
  - entity: number.contabilita_forfettario_ricavi_annui
    name: Ricavi Annui Stimati
  - entity: sensor.contabilita_forfettario_reddito_forfettario
    name: Reddito Forfettario
  - entity: sensor.contabilita_forfettario_contributi_inps
    name: Contributi INPS
  - entity: sensor.contabilita_forfettario_imposta_sostitutiva
    name: Imposta Sostitutiva
  - entity: sensor.contabilita_forfettario_carico_fiscale_reale
    name: Totale Tasse
  - entity: sensor.contabilita_forfettario_utile_netto_stimato
    name: Utile Netto
  - type: section
    label: Acconti
  - entity: sensor.contabilita_forfettario_acconto_giugno
    name: Acconto Giugno
  - entity: sensor.contabilita_forfettario_acconto_novembre
    name: Acconto Novembre
```

## Note Importanti

⚠️ **Questa integrazione è solo a scopo informativo e di stima.**  
Consulta sempre un commercialista per i calcoli ufficiali.

## Supporto

Per bug o richieste di funzionalità, apri una issue su GitHub.

## Licenza

MIT License
