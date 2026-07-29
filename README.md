# Italian Demographic Observatory

Dashboard interattiva sulla demografia italiana, basata su dati **ISTAT** ed **Eurostat**.

📊 **Live**: [https://username.github.io/demographic-dash](https://username.github.io/demographic-dash)

## Caratteristiche

- **Single-file HTML** — nessun backend, database o framework
- **Dati ufficiali** — tutte le serie storiche provengono da ISTAT ed Eurostat
- **Grafici interattivi** — Chart.js con plugin per annotazioni e etichette
- **Indicatori chiave** — KPI aggiornati con CountUp.js
- **Proiezioni demografiche** — scenari ISTAT al 2050
- **Accessibile** — ARIA labels, navigazione tastiera, riduzione movimento
- **GitHub Pages ready** — pubblicazione immediata

## Struttura

```
demographic-dash/
├── index.html               # Dashboard (single file)
├── scripts/
│   └── update_data.py       # Script di aggiornamento dataset
├── docs/
│   ├── DATA_SOURCES.md      # Fonti e metadata
│   ├── ARCHITECTURE.md      # Architettura del progetto
│   ├── UPDATE_WORKFLOW.md   # Procedura di aggiornamento
│   └── CONTRIBUTING.md      # Linee guida contribuzione
├── data/
│   └── dataset.json         # Dataset centralizzato (generato)
└── README.md
```

## Fonti dei dati

| Indicatore | Fonte | Periodo |
|---|---|---|
| Nascite | ISTAT — Bilancio demografico | 1960–2025 |
| TFR | ISTAT — Indicatori demografici | 1960–2025 |
| Popolazione | ISTAT — Popolazione residente | 1960–2025 |
| TFR regionale | ISTAT — Indicatori regionali | 2024 |
| TFR Europa | Eurostat — demo_find | 2024 |
| Proiezioni | ISTAT — Previsioni 2023–2070 | 2025–2050 |

Vedi [DATA_SOURCES.md](./docs/DATA_SOURCES.md) per i dettagli completi.

## Aggiornamento dati

```bash
python scripts/update_data.py
```

Lo script:
1. Verifica e aggiorna il dataset
2. Controlla la coerenza tra serie storiche e tabella
3. Genera report e changelog

Vedi [UPDATE_WORKFLOW.md](./docs/UPDATE_WORKFLOW.md).

## Licenza

- **Dati**: [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) (ISTAT)
- **Codice**: disponibile su GitHub
