# Architecture

## Italian Demographic Observatory

### Overview

```
demographic-dash/
├── index.html          # Dashboard principale (single file, ~1800 lines)
├── scripts/
│   └── update_data.py  # Script python per aggiornare i dati
├── docs/
│   ├── DATA_SOURCES.md    # Fonti e metadata
│   ├── ARCHITECTURE.md    # Questo file
│   ├── UPDATE_WORKFLOW.md # Procedura di aggiornamento
│   └── CONTRIBUTING.md    # Linee guida contribuzione
├── data/               # Dati generati dallo script di aggiornamento
│   └── dataset.json    # Dataset centralizzato (generato)
├── README.md           # Documentazione principale
└── .gitignore
```

### Vincoli architetturali

1. **Single-file HTML**: l'intera applicazione è contenuta in `index.html`
2. **Nessun backend**: tutto client-side, pubblicabile su GitHub Pages
3. **Nessun framework**: HTML/CSS/JS vanilla
4. **Nessuna build pipeline**: nessun bundler, transpiler o preprocessore
5. **CDN per librerie**: Chart.js, plugin, CountUp.js

### Data flow

```
ISTAT / Eurostat (fonti ufficiali)
        │
        ▼
scripts/update_data.py  ← scarica, estrae, verifica
        │
        ▼
data/dataset.json       ← dataset centralizzato
        │
        ▼
index.html              ← dashboard legge dataset.json
```

### Componenti della dashboard

```
HTML
├── Loading overlay
├── Hero section (titolo, descrizione, metadata dataset)
├── Control center (navigazione, filtri)
├── KPI grid (6 indicatori chiave)
├── Main chart (serie storica nascite + TFR)
├── Timeline interattiva
├── Analytical observations
├── Grid-2 (Europa + Regioni)
├── Grid-3 (Età, Proiezioni, Fattori)
├── Data table (database completo)
├── Methodology section
├── Changelog
├── Metadata footer
└── Modal (info/fonti)
```

### Dipendenze CDN

| Libreria | Versione | Utilizzo |
|---|---|---|
| Chart.js | ^4.4 | Grafici interattivi |
| chartjs-plugin-datalabels | ^2.2 | Etichette dati |
| chartjs-plugin-annotation | ^2.2 | Annotazioni (soglia TFR) |
| CountUp.js | ^2.8 | Animazione contatori KPI |

### Modello dati (DATA)

Ogni serie storica nell'oggetto DATA contiene:

```javascript
{
  births: {
    values: [/* array di valori */],
    years: [/* array di anni */],
    metadata: {
      source: "ISTAT - Bilancio demografico",
      sourceUrl: "https://demo.istat.it/",
      period: "1960-2025",
      lastUpdate: "2026-02-15",
      status: "mixed",  // consolidato | provvisorio | stimato
      notes: "Unità: migliaia. Dati 2025 provvisori.",
      version: "1.2"
    }
  },
  // ... altre serie
}
```
