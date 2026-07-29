# Architecture — Italian Demographic Observatory

> Documento di architettura del sistema — descrive la progettazione, i vincoli architetturali, il data flow, la struttura modulare della dashboard e la pipeline di automazione Python.

---

## 1. Filosofia architetturale

L'Osservatorio Demografico Italiano adotta un'architettura **multi-file HTML + Vanilla JS/CSS modulari**, una scelta progettuale che privilegia:

| Principio | Motivazione |
|---|---|
| **Zero dipendenze backend** | Nessun server, database, API o runtime richiesto |
| **Pubblicazione immediata** | Compatibile con GitHub Pages, Netlify, qualsiasi static host |
| **Separazione delle responsabilità** | CSS, JS e HTML in file separati per una manutenzione agevole |
| **Manutenibilità** | Nessuna build pipeline, bundler o transpiler da configurare |
| **Trasparenza scientifica** | I dati sono embedded nel codice, verificabili a colpo d'occhio |
| **Caricamento parallelo** | I file defer permettono il parsing asincrono senza bloccare il rendering |

> **Nota:** Rispetto alla precedente architettura single-file, la separazione fisica dei moduli (`css/`, `js/`) rende il codice più gestibile, testabile e adatto alla collaborazione, senza introdurre complessità di build.

## 2. Vincoli architetturali

1. **HTML + CSS + JS modulari** — l'applicazione è suddivisa in file separati
2. **Nessun backend** — tutto client-side, pubblicabile su qualsiasi hosting statico
3. **Nessun framework** — HTML/CSS/JS vaniglia, zero framework frontend
4. **Nessuna build pipeline** — nessun bundler (Webpack, Vite), transpiler (Babel) o preprocessore (SASS, TypeScript)
5. **CDN per librerie esterne** — Chart.js, CountUp.js caricati da jsdelivr.net
6. **Single Source of Truth** — l'oggetto `DATA` in JavaScript è l'unica fonte di verità dei dati
7. **Moduli JS con `defer`** — caricamento non bloccante, esecuzione sequenziale garantita

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

## 4. Architettura della Dashboard (file separati)

### 4.1 Struttura dei file

```
/
├── index.html              ← Markup HTML semantico (ridotto)
├── css/
│   └── styles.css          ← Tutti gli stili (variabili, layout, responsive, print)
├── js/
│   ├── config.js           ← Metadati, utility (formatNum, showToast, downloadChart, COLORS)
│   ├── kpi.js              ← initKPIs(), initCounters() — animazione CountUp.js
│   ├── charts.js           ← initCharts() — tutti i 6 grafici Chart.js
│   ├── navigation.js       ← initNavigation(), initExport() — scroll, toast
│   ├── modals.js           ← initModals() — focus management WCAG AA
│   └── app.js              ← Entry-point: initTable, initChangelog, initTimeline,
│                              updateMetadata, hideLoadingOverlay + DOMContentLoaded
├── data/
│   └── dataset.json        ← Dataset JSON strutturato
├── scripts/
│   └── update_data.py      ← Pipeline Python di aggiornamento dati
├── docs/
│   ├── ARCHITECTURE.md     ← Questo documento
│   ├── CHANGELOG.md        ← Storico versioni
│   └── UPDATE_WORKFLOW.md  ← Manuale operativo
└── README.md               ← Descrizione progetto
```

### 4.2 Struttura HTML (index.html)

```
index.html  (~650 righe)
│
├── <head>
│   ├── Meta tags (viewport, description, OG, theme-color)
│   ├── Favicon (SVG inline)
│   ├── Google Fonts (preconnect + stylesheet)
│   ├── link rel="stylesheet" href="css/styles.css"
│   ├── CDN Libraries (defer)
│   ├── JS Modules (defer, ordinati)
│   └── <script> const DATA = {…} </script>
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
│   ├── Metadata Footer (fonti, licenze, versioni)
│   ├── Modal Window (info fonti)
│   └── Toast notification
│
└── (nessun tag <script> finale — tutto nei moduli defer)
```

### 4.3 Separazione modulare JS

Tutte le funzioni `init*` sono globali e richiamabili nell'ordine corretto da `app.js`. L'entry point è unico:

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

| Modulo | Funzioni | Responsabilità | Dipendenze |
|---|---|---|---|
| `js/config.js` | `getEl()`, `formatNum()`, `showToast()`, `downloadChart()`, `COLORS`, `barColor()`, `barBorder()` | Utility globali, palette colori gradienti | — |
| `js/kpi.js` | `initKPIs()`, `initCounters()` | Valori statici KPI + animazione CountUp.js | `DATA`, CountUp.js |
| `js/charts.js` | `initChartDefaults()`, `initCharts()` | 6 grafici Chart.js con gradienti dinamici, toggle line/bar, export PNG | `DATA`, Chart.js + plugin |
| `js/navigation.js` | `initNavigation()`, `initExport()` | Scroll fluido con offset, export massivo PNG | — |
| `js/modals.js` | `initModals()` | Modali con focus trap WCAG AA | — |
| `js/app.js` | `initTable()`, `initChangelog()`, `initTimeline()`, `updateMetadata()`, `hideLoadingOverlay()` + entry point `DOMContentLoaded` | Tabella, changelog, timeline, console stats, loading screen, coordinazione | Tutti i moduli precedenti |

### 4.4 Single-Source Data Layer

Il cuore dell'architettura dati è l'oggetto globale `const DATA = { ... }`, embedded nel `<head>` di `index.html`, che funge da **unica fonte di verità** per tutti i componenti della dashboard.

```javascript
const DATA = {
    metadata: {
        dataset_version: "1.4",
        last_update: "2026-07-29",
        license: "CC BY 3.0 IT",
        status: "consolidated",
        notes: "…"
    },
    sources: { /* … */ },
    observations: {
        fertility: { label, unit, years[], values[] },
        births: { label, unit, years[], values[] },
        deaths: { … },
        population: { … },
        elderly_ratio: { … },
        age_structure: { … },
        first_child_age: { value, year },
        fertility_europe: { countries[], values[] },
        fertility_regions: { regions[], values[] },
        projections: { years[], scenarios: { ottimista, base, pessimista } },
        fertility_threshold: { value: 2.1 },
        causes: { categories[], values[] },
        births_decline: { value: -38.5 },
        kpi: { births, tfr, elderly, population, age, decline },
        timeline: { boom, decline1, crisis1, recovery, crisis2, consolidated_2025, partial_2026 }
    },
    historicalTable: [ { periodo, anno, nascite, tfr, natalita, status } ],
    changelog: [ { version, date, changes[] } ]
};
```

**Principio:** ogni funzione `init*` legge dal `DATA` oggetto. Se il dato cambia, aggiornare il blocco `const DATA = ...` in `index.html` (tramite lo script Python `update_data.py --embed`) è sufficiente per propagare la modifica a tutta la dashboard.

## 5. Dipendenze CDN

| Libreria | Versione | CDN | Utilizzo |
|---|---|---|---|
| Chart.js | ^4.4.7 | jsdelivr | Grafici interattivi (5 canvas) |
| chartjs-plugin-datalabels | ^2.2.0 | jsdelivr | Etichette dati sui grafici |
| chartjs-plugin-annotation | ^2.2.1 | jsdelivr | Linea soglia TFR (2.1) e indicatori |
| CountUp.js | ^2.8.0 | jsdelivr | Animazione contatori KPI |

Tutte le librerie sono caricate con l'attributo `defer` per non bloccare il rendering.

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
| **6** | `embed_dataset_in_html()` | Sincronizza `const DATA = {…}` in `index.html` (inline script) |
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
- **Navigazione tastiera** completa (tabindex, focus visible, focus trap nelle modali)
- **`prefers-reduced-motion`** — disabilita animazioni per utenti con disturbi vestibolari
- **Rapporto di contrasto** ≥ 4.5:1 per testi normali
- **Ruoli ARIA** su grafici e tabelle
- **Semantica HTML** appropriata (landmark, heading gerarchici)
- **Focus management** nelle modali con salvataggio/ripristino del focus precedente

## 8. Schema riassuntivo: vista logica dei componenti

```
┌─────────────────────────────────────────────────────────────────┐
│                      INDEX.HTML                                 │
│  (markup semantico ridotto)                                     │
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

┌─────────────────────────────────────────────────────────────┐
│                    MODULI JS (defer)                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  js/config.js  →  getEl, formatNum, showToast, downloadChart│
│  js/kpi.js     →  initKPIs, initCounters (CountUp.js)       │
│  js/charts.js  →  initCharts (Chart.js + plugin)            │
│  js/navigation.js → initNavigation, initExport              │
│  js/modals.js  →  initModals (focus trap)                  │
│  js/app.js     →  initTable, initChangelog, initTimeline,   │
│                   updateMetadata, hideLoading, entry point   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CSS (css/styles.css)                      │
├─────────────────────────────────────────────────────────────┤
│  :root (variabili, palette colori, tipografia)              │
│  Reset & Base, Layout, Header, Navigation, KPI Grid         │
│  Chart Cards, Timeline, Observations, Data Table            │
│  Methodology, Changelog, Footer, Modal, Toast               │
│  Responsive (3 breakpoint), Reduced Motion, Print           │
└─────────────────────────────────────────────────────────────┘
```

---

> **Documento manutenuto come parte del repository.**  
> Ultimo aggiornamento: 2026-07-29 — Versione v1.4 — Refactoring multi-file.
