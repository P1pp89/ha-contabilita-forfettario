# 📊 Home Assistant – Contabilità Forfettario (Italia)

Questo repository fornisce un **Home Assistant Package YAML** per la gestione e la simulazione
della **contabilità in regime forfettario italiano**.

⚠️ **NON è un’integrazione Home Assistant**
- Non compare in *Impostazioni → Integrazioni*
- Non si aggiunge tramite UI
- Non usa `manifest.json` o file `.py`

È una scelta voluta per garantire:
- trasparenza totale dei calcoli
- massima personalizzazione
- nessuna “magia” nascosta

---

## ✨ Funzionalità

- Calcolo **Reddito Forfettario**
- Calcolo **Contributi INPS**
- Calcolo **Imposta Sostitutiva**
- Gestione aliquota **5% / 15%** in base all’anno di inizio attività
- Stima **Utile Netto**
- Supporto a **dati anno precedente**
- Compatibile con **Utility Meter**
- Pronto per dashboard, grafici ed export dati nel futuro aggiornamento

---

Installazione tramite HACS (consigliato)

Step 1

- Apri HACS
- Vai su Impostazioni → Repository personalizzati
- Aggiungi: https://github.com/P1pp89/ha-contabilita-forfettario
- Categoria: YAML
- Conferma e scarica il repository
⚠️ HACS scarica i file, ma non li attiva automaticamente.


Step 2
Nel file configuration.yaml aggiungi se non presente:

homeassistant:

  packages:
  
    contabilita_forfettario: !include contabilita_forfettario.yaml



Step 3
Riavvia Home Assistant per trovare le entità.


Installazione Manuale

- Copia la cartella ha-contabilita-forfettario/ nel tuo percorso homeassistant/custom_component/ di Home Assistant

- Nel file configuration.yaml aggiungi se non presente:

homeassistant:

  packages:
  
    contabilita_forfettario: !include contabilita_forfettario.yaml

- Riavvia Home Assistant


Disclaimer

Questo progetto è uno strumento di supporto.
Non sostituisce un commercialista.
I calcoli sono indicativi e basati su regole generali del regime forfettario italiano.

🤝 Contributi

Pull Request e suggerimenti sono benvenuti.

Il progetto nasce da un’esigenza reale e cresce con l’esperienza sul campo.

