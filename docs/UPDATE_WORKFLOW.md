# Update workflow

## Come aggiornare i dati della dashboard

### 1. Automatizzato (raccomandato)

```bash
python scripts/update_data.py
```

Lo script:
1. Scarica i comunicati ISTAT più recenti
2. Estrae nascite, TFR, popolazione
3. Confronta con i dati esistenti
4. Segnala eventuali discrepanze
5. Aggiorna `data/dataset.json`
6. Genera automaticamente il changelog
7. Stampa un report riepilogativo

Requisiti: Python 3.9+, `pip install requests beautifulsoup4`

### 2. Manuale

Se lo script automatico non è disponibile o fallisce:

1. Consultare le fonti ufficiali (vedi DATA_SOURCES.md)
2. Modificare l'oggetto `DATA` in `index.html`
3. Verificare la coerenza tra grafici, KPI e tabella
4. Aggiornare il changelog
5. Aggiornare i metadata (ultimo aggiornamento, stato)

### Validazione pre-commit

Prima di ogni commit, eseguire:

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
