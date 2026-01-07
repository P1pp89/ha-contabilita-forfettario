# Contabilità Forfettario per Home Assistant

![Icon](icon.png)

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

- `number.anno_inizio_attivita_pi` - Anno inizio attività
- `number.coefficiente_redditivita_pi` - Coefficiente redditività
- `number.contributi_inps_anno_precedente_pi` - Contributi INPS pagati l'anno scorso
- `number.ricavi_annui_pi` - Ricavi annui stimati
- `number.imposta_netta_anno_precedente_pi` - Imposta netta anno precedente

### Sensori Calcolati

#### Calcoli Correnti
- `sensor.ricavi_annui_source` - Ricavi annui (per utility meter)
- `sensor.reddito_forfettario_pi` - Reddito forfettario calcolato
- `sensor.contributi_inps_pi` - Contributi INPS da pagare
- `sensor.aliquota_imposta_forfettario_pi` - Aliquota applicata (5% o 15%)
- `sensor.base_imponibile_imposta_pi` - Base imponibile
- `sensor.imposta_sostitutiva_pi` - Imposta sostitutiva
- `sensor.carico_fiscale_reale_pi` - Totale tasse da pagare
- `sensor.utile_netto_stimato_pi` - Utile netto stimato

#### Anno Precedente
- `sensor.ricavi_pi_anno_precedente` - Ricavi anno scorso
- `sensor.reddito_forfettario_pi_anno_precedente` - Reddito forfettario anno scorso
- `sensor.base_imponibile_pi_anno_precedente` - Base imponibile anno scorso
- `sensor.imposta_netta_pi_anno_precedente` - Imposta netta anno scorso

#### Acconti
- `sensor.acconto_totale_imposta_pi` - Acconto totale da pagare
- `sensor.acconto_giugno_pi` - Acconto di giugno
- `sensor.acconto_novembre_pi` - Acconto di novembre

## Utility Meter

Per tracciare i ricavi anno per anno, aggiungi al tuo `configuration.yaml`:

```yaml
utility_meter:
  ricavi_pi_annui_source_2:
    source: sensor.ricavi_annui_source
    cycle: yearly
```

Questo creerà automaticamente:
- `sensor.sensor.ricavi_annui_source_2_last_year` - Ricavi dell'anno precedente

## Esempio Dashboard

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: 💼 Partita IVA Forfettario
    subtitle: Gestione Contabilità
  - type: custom:mushroom-title-card
    title: 📝 Dati Fiscali
    subtitle: ""
  - type: custom:mushroom-chips-card
    chips:
      - type: entity
        entity: number.ricavi_annui_pi
        icon: mdi:cash-multiple
        icon_color: green
        tap_action:
          action: more-info
      - type: entity
        entity: number.coefficiente_redditivita_pi
        icon: mdi:percent
        icon_color: blue
        tap_action:
          action: more-info
      - type: entity
        entity: number.anno_inizio_attivita_pi
        icon: mdi:calendar-start
        icon_color: purple
        tap_action:
          action: more-info
  - type: custom:mushroom-title-card
    title: 📊 Riepilogo Fiscale
    subtitle: ""
  - type: custom:stack-in-card
    cards:
      - type: custom:mushroom-entity-card
        entity: sensor.reddito_forfettario_pi
        name: Reddito Forfettario
        icon: mdi:calculator
        icon_color: amber
        primary_info: name
        secondary_info: state
        tap_action:
          action: more-info
      - type: custom:mushroom-entity-card
        entity: sensor.contributi_inps_pi
        name: Contributi INPS
        icon: mdi:shield-account
        icon_color: orange
        primary_info: name
        secondary_info: state
        tap_action:
          action: more-info
      - type: custom:mushroom-entity-card
        entity: sensor.imposta_sostitutiva_pi
        name: Imposta Sostitutiva
        icon: mdi:file-document
        icon_color: red
        primary_info: name
        secondary_info: state
        tap_action:
          action: more-info
      - type: custom:mushroom-entity-card
        entity: sensor.aliquota_imposta_forfettario_pi
        name: Aliquota Applicata
        icon: mdi:percent-outline
        icon_color: deep-purple
        primary_info: name
        secondary_info: state
        tap_action:
          action: more-info
  - type: custom:mushroom-title-card
    title: 💰 Totali
    subtitle: ""
  - type: grid
    square: false
    columns: 2
    cards:
      - type: custom:mushroom-entity-card
        entity: sensor.carico_fiscale_reale_pi
        name: Totale Tasse
        icon: mdi:cash-remove
        icon_color: red
        primary_info: name
        secondary_info: state
        layout: vertical
        tap_action:
          action: more-info
        card_mod:
          style: |
            ha-card {
              background: rgba(244, 67, 54, 0.1);
            }
      - type: custom:mushroom-entity-card
        entity: sensor.utile_netto_stimato_pi
        name: Utile Netto
        icon: mdi:cash-check
        icon_color: green
        primary_info: name
        secondary_info: state
        layout: vertical
        tap_action:
          action: more-info
        card_mod:
          style: |
            ha-card {
              background: rgba(76, 175, 80, 0.1);
            }
  - type: custom:mushroom-title-card
    title: 📅 Acconti Fiscali
    subtitle: ""
  - type: custom:mushroom-chips-card
    chips:
      - type: entity
        entity: sensor.acconto_giugno_pi
        icon: mdi:calendar-clock
        icon_color: orange
        content_info: state
        tap_action:
          action: more-info
      - type: entity
        entity: sensor.acconto_novembre_pi
        icon: mdi:calendar-alert
        icon_color: red
        content_info: state
        tap_action:
          action: more-info
      - type: entity
        entity: sensor.acconto_totale_imposta_pi
        icon: mdi:calculator-variant
        icon_color: purple
        content_info: state
        tap_action:
          action: more-info
  - type: custom:mushroom-title-card
    title: 📆 Storico Anno Precedente
    subtitle: ""
  - type: custom:stack-in-card
    cards:
      - type: custom:mushroom-entity-card
        entity: sensor.ricavi_pi_anno_precedente
        name: Ricavi Anno Precedente
        icon: mdi:chart-line
        icon_color: blue
        primary_info: name
        secondary_info: state
      - type: custom:mushroom-entity-card
        entity: sensor.reddito_forfettario_pi_anno_precedente
        name: Reddito Anno Precedente
        icon: mdi:cash-clock
        icon_color: cyan
        primary_info: name
        secondary_info: state
      - type: custom:mushroom-entity-card
        entity: sensor.imposta_netta_pi_anno_precedente
        name: Imposta Anno Precedente
        icon: mdi:file-chart
        icon_color: indigo
        primary_info: name
        secondary_info: state
```

## Note Importanti

⚠️ **Questa integrazione è solo a scopo informativo e di stima.**  
Consulta sempre un commercialista per i calcoli ufficiali.

## Supporto

Per bug o richieste di funzionalità, apri una issue su GitHub.

## Licenza

MIT License
