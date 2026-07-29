# Changelog — Italian Demographic Observatory

> Registro storico delle versioni secondo lo standard [Keep a Changelog](https://keepachangelog.com/).
> Ogni aggiornamento del dataset corrisponde a un incremento di versione (`minor` bump).

---

## [1.4] — 2026-07-29

### Aggiunto
- Nuova serie dati 2026 per `births` (348.000), `fertility` (TFR 1,13), `population` (58,9M)
- Integrazione con lo script `update_data.py`: pipeline automatica di validazione, spike detection e embed
- Documentazione `METHOD.md`: spiegazione rigorosa degli indicatori demografici

### Modificato
- `docs/CHANGELOG.md`: ora generato automaticamente dallo script Python
- `index.html`: il blocco `const DATA = {…}` viene sincronizzato automaticamente via `--embed`

### Tecnologia
- Script Python `update_data.py` con 7 nuovi comandi CLI (`--check`, `--update`, `--embed`, `--simulate`)
- Spike Detection automatica con soglia ±15% YoY per tutte le metriche
- Validazione strutturale dello schema dataset (bloccante all'avvio)

---

## [1.3] — 2026-07-29

### Migliorato
- Reingegnerizzazione completa del data layer: oggetto `DATA` strutturato con metadati e osservazioni
- Refactoring dell'oggetto `DATA` per separare fonti, osservazioni e metadati
- Migliorata la documentazione della struttura dati in `ARCHITECTURE.md`

### Fisso
- Riorganizzazione del dataset JSON per garantire la compatibilità tra `dataset.json` e l'oggetto `DATA` in `index.html`

---

## [1.2] — 2026-02-15

### Aggiunto
- Sezione "Metodologia e fonti" nella dashboard
- Metadati strutturati per ogni serie storica (`source`, `sourceUrl`, `period`, `lastUpdate`, `status`, `notes`)

### Modificato
- Aggiornati dati nascite e TFR al 2025 (dato provvisorio ISTAT)
- Aggiornati dati popolazione residente al 2025

### Fisso
- **Discrepanze tabella/grafico**: corrette le incoerenze nei dati 1976 e 1987 tra la tabella storica e i grafici
- **Allineamento fonti**: dataset allineato ai comunicati ISTAT ufficiali di febbraio 2026

---

## [1.1] — 2025-03-01

### Aggiunto
- Dati 2024 consolidati per nascite, TFR e popolazione
- Metadati su ogni serie storica (fonte, URL, periodo, stato)
- Sezione proiezioni ISTAT (scenario mediano 2025–2050)

### Modificato
- Corretta la fonte delle proiezioni demografiche (da scenario "centrale" a "mediano" secondo nomenclatura ISTAT)

---

## [1.0] — 2025-01-15

### Aggiunto
- 🎉 **Primo rilascio** del dataset strutturato
- Dati storici 1960–2024 da ISTAT per nascite, TFR e popolazione
- Dashboard interattiva con grafici Chart.js, KPI CountUp.js, timeline eventi
- Accessibilità WCAG AA (ARIA labels, navigazione tastiera, contrasto elevato)
- Tabella dati storici completa con ordinamento colonne
- Distribuzione immediata su GitHub Pages

### Tecnologia
- Single-file HTML (~1800 righe) con vaniglia JavaScript e CSS
- Librerie CDN: Chart.js 4.4, CountUp.js 2.8
- Zero dipendenze backend e zero build pipeline

---

<p align="center">
  <sub>Keep a Changelog — https://keepachangelog.com/</sub><br>
  <sub>Ultimo aggiornamento: 2026-07-29</sub>
</p>
