# HA Contabilità Forfettario

Pacchetto Home Assistant per gestire la contabilità di una partita IVA in regime forfettario.

![HACS](https://img.shields.io/badge/HACS-Ready-blue)

## Funzionalità v0.1
- Input helper configurabili:
  - Ricavi annui
  - Coefficiente di redditività
  - Aliquota imposta sostitutiva
  - Aliquota contributi INPS
- Sensori:
  - Reddito imponibile
  - Imposta sostitutiva
  - Contributi INPS
  - Reddito netto stimato

## Installazione manuale
1. Copiare `packages/contabilita_forfettario.yaml` in `config/packages/`
2. Aggiungere in `configuration.yaml`:
```yaml
homeassistant:
  packages: !include_dir_named packages


reboot home assistant

enjoy
