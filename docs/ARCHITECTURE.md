# Architecture — Italian Demographic Observatory

> Documento di architettura del sistema — descrive la progettazione, i vincoli architetturali, il data flow, la struttura modulare della dashboard e la pipeline di automazione Python.

---

## 1. Filosofia architetturale

L'Osservatorio Demografico Italiano adotta un'architettura **Single-File HTML + Vanilla JS/CSS**, una scelta progettuale deliberata che privilegia:

| Principio | Motivazione |
|---|---|
| **Zero dipendenze backend** | Nessun server, database, API o runtime richiesto |
| **Pubblicazione immediata** | Compatibile con GitHub Pages, Netlify, qualsiasi static host |
| **Massima portabilità** | Un singolo file HTML contiene tutto: markup, stili, logica e dati |
| **Manutenibilità** | Nessuna build pipeline, bundler o transpiler da configurare |
| **Trasparenza scientifica** | I dati sono embedded nel codice, verificabili a colpo d'occhio |

> **Trade-off riconosciuto:** L'architettura single-file limita la separazione fisica dei moduli, ma la separazione logica è garantita da funzioni JS ben definite (vedi §4). Per le dimensioni attuali del progetto (~2100 righe), questa scelta è ottimale.

## 2. Vincoli architetturali

1. **Single-file HTML** — l'intera applicazione è contenuta in `index.html`
2. **Nessun backend** — tutto client-side, pubblicabile su qualsiasi hosting statico
3. **Nessun framework** — HTML/CSS/JS vaniglia, zero framework frontend
4. **Nessuna build pipeline** — nessun bundler (Webpack, Vite), transpiler (Babel) o preprocessore (SASS, TypeScript)
5. **CDN per librerie esterne** — Chart.js, CountUp.js caricati da jsdelivr.net
6. **Single Source of Truth** — l'oggetto `DATA` in JavaScript è l'unica fonte di verità dei dati

## 3. Data Flow & Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PIPELINE DI AGGIORNAMENTO DATI                   │
└─────────────────────────────────────────────────────────────────────┘

    ISTAT / Eurostat                         SCRIPT PYTHON
    (fonti ufficiali)                   (scripts/update_data.py)
         │                                       │
         │  Comunicato stampa                     │
         │  (.pdf / .csv / .json)                 │
         ▼                                       │
    ┌──────────────┐                             │
    │ istat_       │   ──load─────────────────►  │
    │ payload.json │                             │
    └──────────────┘                             │
                                                 │
         │  ◄── validate_dataset()               │
         │      Schema validation                 │
         │      Chiavi obbligatorie              │
         │      Coerenza years/values            │
         │                                       │
         │  ◄── sanity_checks()                  │
         │      Range valori                     │
         │      Spike detection (>15% YoY)       │
         │      Gap temporali                    │
         │      Anni duplicati                   │
         │                                       │
         │  ◄── apply_updates()                  │
         │      Aggiunge nuovo anno/valore       │
         │      Incrementa versione (minor)       │
         │      Aggiorna lastUpdate              │
         │      Inserisce changelog              │
         │                                       │
         ▼                                       │
    ┌──────────────────┐                         │
    │ data/dataset.json │ ◄── salva ──────────── │
    └──────────────────┘                         │
         │                                       │
         │  ◄── write_changelog_md()             │
         │      Genera docs/CHANGELOG.md          │
         │                                       │
         │  ◄── embed_dataset_in_html()          │
         │      Sostituisce const DATA = { ... } │
         │      in index.html                    │
         │                                       │
         ▼                                       ▼
    ┌──────────────────┐                 ┌──────────────┐
    │  index.html      │                 │ CHANGELOG.md │
    │  (dashboard)     │                 │ (leggibile)  │
    └──────────────────┘                 └──────────────┘
```

### Flussi secondari (GitHub Actions / CI/CD)

```
┌──────────────┐    ┌──────────────────┐    ┌────────────────┐
│ git push     │──►│ python update    │──►│ git commit     │
│ (payload)    │    │ --update --embed │    │ auto (v1.x)    │
└──────────────┘    └──────────────────┘    └────────────────┘
                                                      │
                                                      ▼
                                              ┌────────────────┐
                                              │ GitHub Pages   │
                                              │ deploy         │
                                              └────────────────┘
```

## 4. Architettura della Dashboard (index.html)

### 4.1 Struttura HTML

```
index.html  (~2100 righe)
│
├── <head>
│   ├── Meta tags (viewport, description, OG, theme-color)
│   ├── Favicon (SVG inline)
│   ├── Google Fonts (preconnect + stylesheet)
│   ├── CDN Libraries (Chart.js, datalabels, annotation, CountUp.js)
│   └── <style> — intero foglio di stile embedded
│
├── <body>
│   ├── Loading overlay (animazione spinner)
│   ├── Observatory Console (hero + badge metadati)
│   ├── Header (titolo, descrizione, indicatori correnti)
│   ├── Control Center (navigazione interna + filtri)
│   ├── KPI Grid (6 contatori animati + note)
│   ├── Main Chart (serie storica nascite + TFR + soglia 2.1)
│   ├── Timeline interattiva (7 eventi demografici)
│   ├── Analytical Observations (testo analitico)
│   ├── Grid-2: Europa + Regioni (TFR comparativo)
│   ├── Grid-3: Età, Proiezioni, Fattori (struttura popolazione)
│   ├── Data Table (DB storico navigabile)
│   ├── Methodology Section (metodologia indicatori)
│   ├── Changelog Section (storico versioni)
│   ├── Metadata Footer (fonti, licenze, versioni)
│   └── Modal Window (info fonti)
│
└── <script> — intera logica applicativa
    ├── const DATA = { ... }           ← dataset embedded
    ├── Utility functions (downloadChart, showToast, formatNum)
    ├── initChartDefaults()            ← tema globale Chart.js
    ├── initCounters()                 ← animazione KPI con CountUp.js
    ├── initKPIs()                     ← valori statici KPI
    ├── initCharts()                   ← tutti i grafici Chart.js
    ├── initTable()                    ← tabella dati ordinabile
    ├── initChangelog()                ← storico versioni
    ├── initNavigation()               ← scroll navigazione
    ├── initExport()                   ← export PNG
    ├── initTimeline()                 ← linea del tempo
    ├── initModals()                   ← finestre modali
    ├── updateMetadata()               ← console stats
    └── DOMContentLoaded → init pipeline
```

### 4.2 Separazione modulare JS

Tutte le funzioni `init*` sono indipendenti e richiamabili in qualsiasi ordine. Il punto di ingresso è unico:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    initKPIs();
    initCounters();
    initCharts();
    initTable();
    initChangelog();
    initNavigation();
    initExport();
    initTimeline();
    initModals();
    updateMetadata();
});
```

| Funzione | Responsabilità | Dipendenze |
|---|---|---|
| `initKPIs()` | Valori statici nei 6 card KPI | `DATA` |
| `initCounters()` | Animazione CountUp.js sui KPI | `DATA`, CountUp.js |
| `initCharts()` | Grafico principale, Europa, Regioni, Proiezioni, Età | `DATA`, Chart.js + plugin |
| `initTable()` | Tabella dati storici con ordinamento colonne | `DATA` |
| `initChangelog()` | Sezione storico versioni | `DATA.changelog` |
| `initNavigation()` | Scroll fluido e highlight sezione attiva | — |
| `initExport()` | Download grafico come PNG | — |
| `initTimeline()` | Timeline interattiva 7 eventi | `DATA.historicalTable` |
| `initModals()` | Apertura/chiusura modale fonti | — |
| `updateMetadata()` | Console stats (versione, data, indicatori) | `DATA` |

### 4.3 Single-Source Data Layer

Il cuore dell'architettura dati è l'oggetto globale `const DATA = { ... }`, che funge da **unica fonte di verità** per tutti i componenti della dashboard.

```javascript
const DATA = {
    // Metadati
    metadata: {
        dataset_version: "1.3",
        last_update: "2026-07-29",
        license: "CC BY 3.0 IT",
        status: "mixed",
        notes: "…"
    },
    // Serie principali (top-level per accesso rapido)
    births: {
        label: "Nati vivi",
        unit: "migliaia",
        years: [1960, 1961, …, 2025],
        values: [950, 960, …, 355],
        source: "births"
    },
    fertility: { /* … */ },
    population: { /* … */ },

    // Osservazioni strutturate (sotto-chiave unique)
    observations: {
        fertility: { /* TFR completo */ },
        births: { /* nascite */ },
        population: { /* popolazione */ },
        elderly_ratio: { /* % over 65 */ },
        age_structure: { /* piramide età */ },
        first_child_age: { /* età media primo figlio */ },
        fertility_europe: { /* confronto UE */ },
        fertility_regions: { /* confronto regionale */ },
        projections: { /* 3 scenari ISTAT */ }
    },

    // Tabella eventi storici
    historicalTable: [
        { periodo: "Baby Boom", anno: "1964-65", nascite: 1050000, tfr: 2.55, … },
        // …
    ],

    // Storico versioni
    changelog: [
        { version: "1.2", date: "2026-02-15", changes: […] },
        // …
    ]
};
```

**Principio:** ogni `init*` funzione legge dal `DATA` oggetto. Se il dato cambia, aggiornare `DATA` è sufficiente per propagare la modifica a tutta la dashboard. Questo è garantito meccanicamente dallo script `update_data.py` che embedda automaticamente il JSON in index.html.

## 5. Dipendenze CDN

| Libreria | Versione | CDN | Utilizzo |
|---|---|---|---|
| Chart.js | ^4.4.7 | jsdelivr | Grafici interattivi (5 canvas) |
| chartjs-plugin-datalabels | ^2.2.0 | jsdelivr | Etichette dati sui grafici |
| chartjs-plugin-annotation | ^2.2.1 | jsdelivr | Linea soglia TFR (2.1) e indicatori |
| CountUp.js | ^2.8.0 | jsdelivr | Animazione contatori KPI |

## 6. Automation Pipeline (Python)

### 6.1 Script: `scripts/update_data.py`

Script Python 3.9+ **senza dipendenze esterne** (sola libreria standard). Pipeline completa:

| Fase | Funzione | Descrizione |
|---|---|---|
| **1** | `load_istat_payload()` | Legge il file `data/istat_payload.json` con le nuove osservazioni |
| **2** | `validate_dataset()` | Validazione strutturale dello schema dataset (bloccante) |
| **3** | `sanity_checks()` | Controlli anomalie: range, spike YoY, gap, duplicati (warning) |
| **4** | `apply_updates()` | Applica nuovi valori, incrementa versione, scrive changelog |
| **5** | `write_changelog_md()` | Genera `docs/CHANGELOG.md` in Markdown |
| **6** | `embed_dataset_in_html()` | Sincronizza `const DATA = {…}` in `index.html` |
| **7** | `generate_report()` | Report finale a terminale |

### 6.2 CLI: comandi

| Comando | Azione |
|---|---|
| `python scripts/update_data.py` | Mostra help |
| `--check` | Validazione dry-run (nessuna modifica) |
| `--update` | Aggiorna `dataset.json` + genera changelog |
| `--embed` | Aggiorna dataset + sincronizza `index.html` |
| `--simulate` | Forza uso di payload simulato (test) |

Vedi [UPDATE_WORKFLOW.md](./UPDATE_WORKFLOW.md) per il manuale operativo completo.

## 7. Accessibilità (WCAG AA)

Il sistema è progettato per soddisfare le linee guida WCAG 2.1 Livello AA:

- **ARIA labels** su tutti gli elementi interattivi
- **Navigazione tastiera** completa (tabindex, focus visible)
- **`prefers-reduced-motion`** — disabilita animazioni per utenti con disturbi vestibolari
- **Rapporto di contrasto** ≥ 4.5:1 per testi normali
- **Ruoli ARIA** su grafici e tabelle
- **Semantica HTML** appropriata (landmark, heading gerarchici)

## 8. Schema riassuntivo: vista logica dei componenti

```
┌─────────────────────────────────────────────────────────────────┐
│                      INDEX.HTML                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐ │
│  │   KPI    │   │  Charts  │   │  Table   │   │  Nav/Modal  │ │
│  │  Grid    │   │  (5 ctx) │   │ (sorted) │   │  /Export    │ │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └──────┬──────┘ │
│       │              │              │                │         │
│       └──────────────┴──────┬───────┴────────────────┘         │
│                             │                                   │
│                      ┌──────▼──────┐                           │
│                      │   const     │                           │
│                      │ DATA = {…}  │  ← Single Source of Truth│
│                      └─────────────┘                           │
│                             ▲                                   │
│                             │ (embed automatico)                 │
│                      ┌──────┴──────┐                           │
│                      │ dataset.json│                           │
│                      └─────────────┘                           │
│                             ▲                                   │
│                             │ (update_data.py)                  │
│                      ┌──────┴──────┐                           │
│                      │   ISTAT     │                           │
│                      │  Eurostat   │                           │
│                      └─────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

> **Documento manutenuto come parte del repository.**  
> Ultimo aggiornamento: 2026-07-29 — Versione v1.4.
