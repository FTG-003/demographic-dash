# Update workflow

## Come aggiornare i dati della dashboard

### 1. Automatizzato (raccomandato)

```bash
# Aggiorna solo dataset (aggiorna lastUpdate, salva dataset.json)
python scripts/update_data.py

# Aggiorna dataset + sincronizza index.html
python scripts/update_data.py --embed

# Solo validazione (nessuna modifica)
python scripts/update_data.py --check
```

Lo script:
1. Carica `data/dataset.json` come **unica fonte di verità**
2. Valida automaticamente lo schema del dataset (chiavi obbligatorie, coerenza anni/valori, scenari)
3. Aggiorna `lastUpdate` con la data odierna
4. Salva il dataset aggiornato
5. Se `--embed` è passato, sincronizza il blocco `const DATA = { ... };` dentro `index.html`
   usando parsing a bilanciamento di graffe (supporta oggetti annidati multilinea)

**Requisiti:** Python 3.9+ (sola libreria standard — nessuna dipendenza esterna)

### 2. Cosa verifica la validazione

La funzione `validate_dataset()` controlla:

- **Chiavi di primo livello**: `version`, `license`, `sources`, `observations`
- **Observations obbligatorie**: `births`, `fertility`, `population`, `elderly_ratio`, `first_child_age`
- **Scenari**: `observations.projections.scenarios` — deve essere un oggetto non vuoto
- **Coerenza**: ogni serie temporale (`births`, `fertility`, `population`) deve avere
  array `years` e `values` della stessa lunghezza
- **Campi specifici**: `first_child_age.value` e `first_child_age.year` devono esistere

### 3. Workflow tipico pre-commit

```bash
# 1. Verifica che il dataset sia valido
python scripts/update_data.py --check

# 2. Se ok, aggiorna dataset + HTML
python scripts/update_data.py --embed

# 3. Committa entrambi i file
git add data/dataset.json index.html
git commit -m "Aggiornamento dati demografici"
```

### 4. Validazione pre-commit (aggiuntiva)

```bash
# Verifica HTML
npx html-validate index.html

# Verifica console (aprire in browser)
# - Nessun errore JS
# - Nessun warning

# Verifica responsive
# Testare a width: 375px, 768px, 1440px

# Verifica dati
# - KPI corrispondono ai grafici
# - Grafici corrispondono alla tabella
# - Anni e valori coerenti

# Verifica accessibilità basica
# - Contrasto sufficiente
# - ARIA labels presenti
# - Navigazione tab funzionante
```

### 5. Manutenzione dataset

Lo script **non** contiene più un `DEFAULT_DATASET` hardcodato.
`data/dataset.json` è l'unica fonte di verità. Per modificare i dati:

1. Editare direttamente `data/dataset.json`
2. Eseguire `python scripts/update_data.py --check` per validare
3. Eseguire `python scripts/update_data.py --embed` per propagare su HTML

### 6. Struttura del dataset

```
{
  "version": "x.y",
  "lastUpdate": "YYYY-MM-DD",
  "license": "CC BY 3.0 IT",
  "sources": { ... },
  "observations": {
    "births":          { "years": [...], "values": [...] },
    "fertility":       { "years": [...], "values": [...] },
    "population":      { "years": [...], "values": [...] },
    "elderly_ratio":   { "years": [...], "values": [...] },
    "age_structure":   { ... },
    "first_child_age": { "value": ..., "year": ... },
    "fertility_europe":   { ... },
    "fertility_regions":  { ... },
    "projections":    { "years": [...], "scenarios": { ... } }
  },
  "historicalTable": [ ... ],
  "changelog": [ ... ]
}
```
