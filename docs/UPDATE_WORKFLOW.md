# Update Workflow — Italian Demographic Observatory

> Flusso di lavoro completo per l'aggiornamento automatizzato dei dati demografici
> da comunicati ISTAT, con validazione, versioning, changelog e sincronizzazione HTML.

---

## Indice

1. [Prerequisiti](#1-prerequisiti)
2. [Struttura dei file](#2-struttura-dei-file)
3. [Payload ISTAT (input)](#3-payload-istat-input)
4. [CLI: comandi disponibili](#4-cli-comandi-disponibili)
5. [Pipeline di aggiornamento](#5-pipeline-di-aggiornamento)
6. [Regole di validazione](#6-regole-di-validazione)
7. [Versionamento & Changelog](#7-versionamento--changelog)
8. [Esempi d'uso](#8-esempi-duso)
9. [Manutenzione & risoluzione problemi](#9-manutenzione--risoluzione-problemi)

---

## 1. Prerequisiti

- **Python 3.9+** (sola libreria standard — nessuna dipendenza esterna)
- Repository clonato con struttura standard:

```
demographic-dash/
├── data/
│   ├── dataset.json            # Dataset JSON (unica fonte di verità)
│   └── istat_payload.json      # Payload ISTAT (opzionale, input nuovo dato)
├── docs/
│   ├── CHANGELOG.md            # Changelog in formato Markdown (generato)
│   └── UPDATE_WORKFLOW.md      # Questo file
├── scripts/
│   └── update_data.py          # Script di aggiornamento
├── index.html                  # Dashboard HTML (sincronizzato via --embed)
└── README.md
```

---

## 2. Struttura dei file

### `data/dataset.json`

Dataset strutturato contenente:
- `version`: versione corrente (es. `"1.3"`)
- `lastUpdate`: data ultimo aggiornamento
- `license`: licenza dei dati
- `sources`: oggetto con le fonti dati
- `observations`: serie storiche e osservazioni
- `historicalTable`: tabella eventi storici
- `changelog`: registro delle modifiche

### `scripts/update_data.py`

Script principale con le seguenti funzioni:

| Funzione | Descrizione |
|---|---|
| `load_istat_payload()` | Carica payload ISTAT da file JSON |
| `generate_simulated_payload()` | Genera payload simulato per test |
| `sanity_checks()` | Controlli automatici su valori fuori scala, spike YoY, chiavi mancanti |
| `validate_dataset()` | Validazione struttura completa del dataset |
| `apply_updates()` | Applica nuove osservazioni, incrementa versione, aggiorna metadati |
| `generate_changelog_md()` | Genera `docs/CHANGELOG.md` dal changelog interno |
| `embed_dataset_in_html()` | Sincronizza il blocco `const DATA = {...}` in `index.html` |
| `generate_report()` | Stampa report formale nel terminale |

---

## 3. Payload ISTAT (input)

I nuovi dati arrivano tramite un file JSON in `data/istat_payload.json` con questa struttura:

```json
{
  "source_note": "ISTAT - Bilancio demografico 2026",
  "update_type": "annuale",
  "observations": {
    "births": {
      "year": 2026,
      "value": 348000
    },
    "fertility": {
      "year": 2026,
      "value": 1.14
    },
    "population": {
      "year": 2026,
      "value": 58.8
    }
  },
  "notes": "Dato provvisorio, comunicato stampa ISTAT del ..."
}
```

**Campi accettati in `observations`:**
- `births` — nati vivi (valore assoluto)
- `fertility` — TFR (figli per donna)
- `population` — popolazione residente (milioni)
- Qualsiasi altra chiave presente nel dataset

Se il file `istat_payload.json` non esiste, lo script genera automaticamente un **payload simulato** basato sui trend storici (utile per test).

---

## 4. CLI: comandi disponibili

| Comando | Azione |
|---|---|
| `python scripts/update_data.py` | Mostra help con tutte le flag disponibili |
| `python scripts/update_data.py --check` | **Validazione dry-run** — carica payload, esegue sanity checks, stampa report. Nessuna modifica. |
| `python scripts/update_data.py --update` | **Aggiornamento dataset** — carica payload, sanity checks, applica modifiche a `dataset.json`, genera `CHANGELOG.md` |
| `python scripts/update_data.py --embed` | **Aggiornamento dataset + sincronizzazione HTML** |
| `python scripts/update_data.py --simulate` | Forza uso di payload simulato (combinabile con `--check`, `--update`) |
| `python scripts/update_data.py --update --embed` | **Full pipeline** — payload → dataset → HTML |

### Combinazioni comuni

```bash
# 1. Test rapido (solo validazione)
python scripts/update_data.py --check --simulate

# 2. Verifica con payload reale
python scripts/update_data.py --check

# 3. Aggiornamento completo
python scripts/update_data.py --update --embed

# 4. Aggiornamento simulato (per test)
python scripts/update_data.py --update --embed --simulate
```

---

## 5. Pipeline di aggiornamento

Il flusso completo (`--update --embed`) esegue questi passi:

```
┌──────────────────┐
│  1. Carica        │
│  dataset.json     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  2. Valida        │◀── validate_dataset()
│  schema dataset   │    (se fallisce → exit)
└────────┬─────────┘
         ↓
┌──────────────────┐
│  3. Carica        │◀── load_istat_payload()
│  payload ISTAT    │    o generate_simulated_payload()
└────────┬─────────┘
         ↓
┌──────────────────┐
│  4. Sanity checks │◀── sanity_checks()
│  (anomalie, spike,│    (warning, non bloccante)
│   range, gap)     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  5. Applica       │◀── apply_updates()
│  aggiornamenti    │    • Aggiunge nuovi valori
│                   │    • Incrementa versione
│                   │    • Aggiorna lastUpdate
│                   │    • Genera changelog
└────────┬─────────┘
         ↓
┌──────────────────┐
│  6. Salva         │
│  dataset.json     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  7. Genera        │◀── write_changelog_md()
│  CHANGELOG.md     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  8. Sincronizza   │◀── embed_dataset_in_html()
│  index.html       │    (solo se --embed)
└────────┬─────────┘
         ↓
┌──────────────────┐
│  9. Report        │◀── generate_report()
│  finale           │
└──────────────────┘
```

---

## 6. Regole di validazione

### 6.1 Validazione strutturale (`validate_dataset()`)

Controlli bloccanti (errore → script termina):

| Controllo | Descrizione |
|---|---|
| Chiavi primo livello | `version`, `license`, `sources`, `observations` obbligatorie |
| Observations obbligatorie | `births`, `fertility`, `population`, `elderly_ratio`, `first_child_age` |
| Proiezioni | `observations.projections.scenarios` deve esistere ed essere un dict non vuoto |
| Coerenza serie | Ogni serie temporale deve avere `years` e `values` della stessa lunghezza |
| elderly_ratio | years/values coerenti |
| first_child_age | `value` e `year` obbligatori |

### 6.2 Sanity checks (`sanity_checks()`)

Controlli non bloccanti (warning, l'aggiornamento procede comunque):

| Controllo | Soglia | Esempio |
|---|---|---|
| **Range valori** | births: [0, 2M], fertility: [0, 5], population: [0, 100], elderly: [0, 100], first_child_age: [15, 50] | births=3_000_000 → warning |
| **Spike YoY** | Variazione % > ±15% | births: 370K → 500K (+35%) → warning |
| **Anno duplicato** | Se l'anno è già presente nel dataset | births 2025 già presente → warning |
| **Gap temporale** | Se il nuovo anno salta uno o più anni | ultimo 2024, nuovo 2026 → warning |
| **Chiavi mancanti** | Observations obbligatorie assenti | `elderly_ratio` missing → warning |

---

## 7. Versionamento & Changelog

### Versione

- Formato: `major.minor` (es. `1.3` → `1.4`)
- Incremento automatico: `minor + 1` a ogni aggiornamento
- La versione viene aggiornata sia in `version` che in `metadata.dataset_version`

### Changelog

Due formati sincronizzati automaticamente:

1. **`data/dataset.json`** → array `changelog` (fonte primaria)
2. **`docs/CHANGELOG.md`** → file Markdown generato (leggibile)

Ogni voce contiene:
```json
{
  "version": "1.4",
  "date": "2026-07-30",
  "changes": [
    "Aggiunto dato births: 348000 (anno 2026)",
    "Aggiunto dato fertility: 1.14 (anno 2026)"
  ]
}
```

---

## 8. Esempi d'uso

### 8.1 Test iniziale (consigliato)

```bash
# Verifica che lo script e il dataset siano funzionanti
python scripts/update_data.py --check --simulate
```

### 8.2 Aggiornamento con payload simulato

```bash
python scripts/update_data.py --update --embed --simulate
```

### 8.3 Aggiornamento con payload reale

```bash
# 1. Prepara il file data/istat_payload.json con i nuovi dati
# 2. Esegui
python scripts/update_data.py --update --embed
```

### 8.4 Validazione pre-commit

```bash
# 1. Verifica
python scripts/update_data.py --check

# 2. Se OK, aggiorna
python scripts/update_data.py --update --embed

# 3. Controlla le differenze
git diff data/dataset.json index.html docs/CHANGELOG.md

# 4. Committa
git add -A
git commit -m "Aggiornamento dati demografici v$(python3 -c "import json; print(json.load(open('data/dataset.json'))['version'])")"
```

### 8.5 Uso in CI/CD

```yaml
# Esempio GitHub Action (pipeline di aggiornamento)
steps:
  - uses: actions/checkout@v4
  - name: Update demographic data
    run: |
      python scripts/update_data.py --update --embed
  - name: Commit changes
    run: |
      git config user.name "Automated Update"
      git config user.email "bot@example.com"
      git add -A
      git commit -m "Automated data update" || echo "No changes"
      git push
```

---

## 9. Manutenzione & risoluzione problemi

### Errori comuni

| Errore | Causa | Soluzione |
|---|---|---|
| `Dataset non trovato: data/dataset.json` | File mancante | Creare `data/dataset.json` con struttura attesa |
| `Chiave 'version' mancante` | Dataset corrotto | Rigenerare da backup o template |
| `Payload non trovato` | `istat_payload.json` assente | Usare `--simulate` per test |
| `Validazione fallita` | Schema non conforme | Verificare controlli in §6.1 |
| `Spike detection` | Variazione >15% | Verificare il dato, se reale forzare l'aggiornamento |

### Test manuali

```bash
# Test payload con spike (valore anomalo)
cat > data/istat_payload.json << 'EOF'
{
  "source_note": "Test spike detection",
  "update_type": "test",
  "observations": {
    "births": {"year": 2026, "value": 500000}
  }
}
EOF
python scripts/update_data.py --check

# Test payload fuori range
cat > data/istat_payload.json << 'EOF'
{
  "source_note": "Test range",
  "update_type": "test",
  "observations": {
    "fertility": {"year": 2026, "value": 12.5}
  }
}
EOF
python scripts/update_data.py --check
```

### Rollback

Per tornare a una versione precedente del dataset:

```bash
# Usa git per ripristinare
git checkout HEAD~1 -- data/dataset.json index.html docs/CHANGELOG.md
```

---

## Appendice: Formato payload supportato

Lo script accetta due formati per le osservazioni nel payload:

### Formato standard (consigliato)
```json
"births": { "year": 2026, "value": 348000 }
```

### Formato esteso (con metadati)
```json
"births": {
  "year": 2026,
  "value": 348000,
  "label": "Nati vivi",
  "unit": "migliaia",
  "notes": "Dato provvisorio ISTAT"
}
```

In formato esteso, se `label` e `unit` vengono forniti, lo script li userà per
aggiornare la struttura dell'observation nel dataset.

---

> **Documento generato automaticamente.** Ultima modifica: 2026-07-30.
> Per aggiornamenti allo script, modificare `scripts/update_data.py` e rigenerare
> questa documentazione.
