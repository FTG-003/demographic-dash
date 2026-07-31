# Italian Demographic Observatory

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License MIT">
  <img src="https://img.shields.io/badge/Version-1.6-brightgreen.svg?style=for-the-badge" alt="Version 1.6">
  <img src="https://img.shields.io/badge/Status-Production-0066cc.svg?style=for-the-badge" alt="Status: Production">
  <img src="https://img.shields.io/badge/WCAG-AA-007F3E.svg?style=for-the-badge" alt="WCAG AA">
  <img src="https://img.shields.io/badge/Stack-HTML5%20%7C%20JS%20%7C%20Chart.js-E34F26.svg?style=for-the-badge" alt="Stack: HTML5/JS/Chart.js">
</p>

---

**L'Osservatorio Demografico Italiano** è una dashboard interattiva, professionale e accessibile per l'analisi della demografia italiana dal 1960 al 2026, basata esclusivamente su **fonti ufficiali ISTAT ed Eurostat**. Il progetto adotta un'architettura single-file HTML con vaniglia JavaScript/CSS, zero dipendenze backend e pubblicazione immediata su GitHub Pages.

---

## Caratteristiche chiave

| Caratteristica | Dettaglio |
|---|---|
| **Grafici interattivi** | Chart.js 4.4 con plugin per annotazioni, etichette dati e soglia TFR (2.1) |
| **KPI animati** | CountUp.js per 6 indicatori chiave aggiornati in tempo reale |
| **Accessibilità WCAG AA** | ARIA labels, navigazione tastiera, `prefers-reduced-motion`, contrasto elevato |
| **Single-Source Data Layer** | Oggetto `DATA` centralizzato — unico punto di verità per tutta la dashboard |
| **Timeline storica** | 7 eventi demografici fondamentali (Baby Boom → Minimo storico 2024) |
| **Proiezioni ISTAT** | 3 scenari (base, ottimista, pessimista) al 2050 |
| **Confronto europeo** | TFR per 7 paesi UE, grafico regionale italiano |
| **Tabella dati completa** | Database storico navigabile con ordinamento colonne |
| **Zero backend** | Pubblicabile su GitHub Pages, CDN per librerie |
| **Automazione Python** | Script `update_data.py` con sanity check, spike detection, changelog automatico |

## Architettura & Tech Stack

```
                  ┌───────────────────────┐
                  │   Fonti Ufficiali      │
                  │   ISTAT / Eurostat     │
                  └──────────┬────────────┘
                             │
                  ┌──────────▼────────────┐
                  │ scripts/update_data.py│  ← Python 3.9+, stdlib only
                  │  (validazione, embed) │
                  └──────────┬────────────┘
                             │
                  ┌──────────▼────────────┐
                  │  data/dataset.json    │  ← Single Source of Truth
                  └──────────┬────────────┘
                             │
                  ┌──────────▼──────────────────────────────────┐
                  │  index.html  +  css/styles.css  +  js/*.js  │
                  │  (Struttura modulare multi-file)             │
                  │  js/config.js · js/kpi.js · js/charts.js    │
                  │  js/navigation.js · js/modals.js · js/app.js│
                  └─────────────────────────────────────────────┘
```

| Livello | Tecnologia | Ruolo |
|---|---|---|
| **Frontend** | HTML5 + Vanilla JS + CSS3 (struttura modulare multi-file) | Single-page application, 6 moduli JS + 1 CSS |
| **Grafici** | Chart.js 4.4.7 + plugin (datalabels 2.2, annotation 2.2) | Grafici interattivi soglia TFR |
| **KPI** | CountUp.js 2.8.0 | Animazione contatori numerici |
| **Font** | DM Serif Display + Inter + JetBrains Mono | Tipografia professionale |
| **Dati** | `data/dataset.json` (JSON strutturato) | Unico data layer centralizzato |
| **Automazione** | Python 3.9+ (sola stdlib) | Script `update_data.py` con pipeline CLI |
| **Distribuzione** | GitHub Pages / qualsiasi static host | Zero configurazione |
| **SEO & GEO** | `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt` | Ottimizzazione motori di ricerca e AI |

## Guida rapida all'avvio

```bash
# 1. Clona il repository
git clone https://github.com/FTG-003/demographic-dash.git
cd demographic-dash

# 2. Avvia un server HTTP locale (Python)
python3 -m http.server 8000

# 3. Apri nel browser
open http://localhost:8000
```

Non è richiesta alcuna build pipeline, bundler o installazione di dipendenze Node.js per il frontend. Le librerie CDN sono caricate direttamente da `jsdelivr.net`.

## Struttura del repository

```
demographic-dash/
│
├── index.html                  # Markup HTML semantico (ridotto, ~650 righe)
├── README.md                   # Questo file — overview enterprise
│
├── css/
│   └── styles.css              # Tutti gli stili (variabili, layout, responsive, print)
│
├── js/
│   ├── config.js               # Metadati, utility (formatNum, showToast, downloadChart, COLORS)
│   ├── kpi.js                  # initKPIs(), initCounters() — animazione CountUp.js
│   ├── charts.js               # initCharts() — tutti i 6 grafici Chart.js
│   ├── navigation.js           # initNavigation(), initExport() — scroll, toast
│   ├── modals.js               # initModals() — focus management WCAG AA
│   └── app.js                  # Entry-point: initTable, initChangelog, initTimeline,
│                               #   updateMetadata, hideLoadingOverlay + DOMContentLoaded
│
├── data/
│   └── dataset.json            # Dataset centralizzato JSON (singola fonte di verità)
│
├── docs/
│   ├── ARCHITECTURE.md         # Architettura del sistema e data flow
│   ├── CHANGELOG.md            # Registro storico versioni (Keep a Changelog)
│   ├── CONTRIBUTING.md         # Linee guida per contribuire
│   ├── DATA_SOURCES.md         # Metodologia e fonti dati (ISTAT/Eurostat)
│   ├── METHOD.md               # Spiegazione indicatori demografici
│   └── UPDATE_WORKFLOW.md      # Manuale operativo script Python
│
├── scripts/
│   └── update_data.py          # Pipeline Python: validazione → update → embed
│
├── robots.txt                  # Istruzioni crawler SEO
├── sitemap.xml                 # Sitemap XML per motori di ricerca
├── llms.txt                    # Guida AI/LLM per l'indicizzazione
├── llms-full.txt               # Versione estesa llms.txt
├── .gitignore
└── package.json                # (Solo metadati, nessuna dipendenza frontend)
```

### SEO & GEO Optimization

Il repository include file specializzati per massimizzare la rilevabilità nei motori di ricerca tradizionali (SEO) e nei sistemi di AI/LLM (GEO — Generative Engine Optimization):

| File | Scopo |
|---|---|
| `robots.txt` | Istruzioni per crawler — aree consentite/disabilitate |
| `sitemap.xml` | Sitemap XML per indicizzazione motori di ricerca |
| `llms.txt` | Guida strutturata per AI/LLM — riepilogo per l'indicizzazione AI |
| `llms-full.txt` | Versione estesa di `llms.txt` con contenuto completo per AI |

Questi file garantiscono che il progetto sia correttamente indicizzato sia dai motori di ricerca tradizionali (Google, Bing) sia dai modelli linguistici di grandi dimensioni (LLM) e dai sistemi RAG.

## Fonti dati & rigore scientifico

Tutti i dati provengono da fonti statistiche ufficiali e sono classificati per stato di consolidamento:

| Indicatore | Fonte | Periodo | Stato |
|---|---|---|---|
| Nascite | ISTAT — Bilancio demografico | 1960–2026 | ✅ Consolidato 1960–2025 / ⚠️ Parziale 2026 |
| TFR | ISTAT — Indicatori demografici | 1960–2026 | ✅ Consolidato 1960–2025 / ⚠️ Parziale 2026 |
| Popolazione residente | ISTAT — Popolazione residente | 1960–2026 | ✅ Consolidato 1960–2025 / ⚠️ Parziale 2026 |
| TFR regionale | ISTAT — Indicatori regionali | 2024 | ✅ Consolidato |
| TFR Europa | Eurostat — demo_find | 2024 | ✅ Consolidato |
| Proiezioni demografiche | ISTAT — Previsioni 2023–2070 | 2025–2050 | 🔮 Previsionale (scenario mediano) |

> **Legenda:** ✅ Consolidato = dato definitivo pubblicato; ⚠️ Provvisorio = stima preliminare; 🔮 Previsionale = proiezione statistica.

Per il dettaglio metodologico completo: [DATA_SOURCES.md](./docs/DATA_SOURCES.md) e [METHOD.md](./docs/METHOD.md).

## Aggiornamento dati

```bash
# Validazione dry-run (nessuna modifica)
python scripts/update_data.py --check

# Aggiornamento completo del dataset + sincronizzazione HTML
python scripts/update_data.py --update --embed

# Test con dati simulati
python scripts/update_data.py --check --simulate
```

Lo script esegue automaticamente:
1. **Sanity checks** su range valori, spike YoY (>±15%), gap temporali e chiavi mancanti
2. **Validazione strutturale** dello schema dataset
3. **Incremento automatico** della versione (minor bump)
4. **Generazione del changelog** in formato Markdown
5. **Embed automatico** del dataset aggiornato in `index.html`

Vedi [UPDATE_WORKFLOW.md](./docs/UPDATE_WORKFLOW.md) per il manuale operativo completo.

## Contributi

I contributi sono benvenuti! Vedi [CONTRIBUTING.md](./docs/CONTRIBUTING.md) per le linee guida.

## Licenza

- **Codice:** [MIT](./LICENSE) © 2025–2026 Italian Demographic Observatory
- **Dati:** [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) (ISTAT) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (Eurostat)
- **Fonti:** ISTAT — Istituto Nazionale di Statistica · Eurostat — Ufficio Statistico dell'Unione Europea

---

<p align="center">
  <sub>Costruito con ❤️ e dati aperti. I dati demografici raccontano la storia di un paese.</sub><br>
  <sub><strong>v1.6</strong> — Rilasciato il 31 Luglio 2026 — Dataset 1.6 — Dati 2025 consolidati ISTAT</sub>
</p>
