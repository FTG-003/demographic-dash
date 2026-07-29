# Changelog — Italian Demographic Observatory

> Registro storico delle versioni secondo lo standard [Keep a Changelog](https://keepachangelog.com/).
> Ogni aggiornamento del dataset corrisponde a un incremento di versione (`minor` bump).

---

## [1.4] — 2026-07-29

### Aggiunto
- Integrazione dati ISTAT **consolidati 2025**: 355.000 nascite, TFR 1,14, Popolazione 58,94 milioni
- Aggiunte **proiezioni parziali 2026**: 340.000 nascite, TFR 1,12, Popolazione 58,82 milioni
- Dataset portato a stato `"consolidated"` con note metodologiche trasparenti
- Nuove voci nella `historicalTable` per 2025 e 2026
- Nuovi eventi nella timeline: `consolidated_2025`, `partial_2026`
- Aggiornati KPI `births.trend` (−66,2%), `tfr.trend` (minimo storico assoluto), `decline` (577K→355K)

### Migliorato
- Periodo fonti esteso a 1960–2026 per births, fertility, population
- Dati popolazione 2025 rettificati a 58,94M (consolidato ISTAT)
- Aggiornati badge e titolo dashboard a v1.4

### Fisso
- **Bonifica Red Team completa (R01–R16)**:
  - R01: Validazione lato server per payload ISTAT
  - R02: Rigore metodologico e trasparenza note
  - R03: Coerenza versione su tutte le superfici
  - R04: Robustezza caricamento CDN (fallback)
  - R05: Performance e lazy loading
  - R06: Sanity check su spike YoY e gap temporali
  - R07: Accessibilità WCAG — label, contrasto, navigazione
  - R08: Gestione errori e boundary
  - R09: Cache busting e versione dinamica
  - R10: Test cross-browser e responsività
  - R11: Codice hardening (XSS, injection)
  - R12: Separazione dati/presentazione
  - R13: Logging e audit trail
  - R14: Documentazione aggiornata
  - R15: Compatibilità backward dataset
  - R16: Allineamento semantico schema

- Sincronizzazione automatica `dataset.json` ↔ `index.html` completata
- Nessuna regressione DOM, dashboard o responsività

---

## [1.3] — 2026-07-29

### Aggiunto
- Nuova sezione `causes` e `fertility_threshold` nelle osservazioni del dataset
- Aggiunti dati `timeline` e `kpi` descrittivi nel dataset per coerenza con `index.html`

### Migliorato
- Reingegnerizzazione completa del data layer: oggetto `DATA` strutturato con metadati e osservazioni
- Refactoring dell'oggetto `DATA` per separare fonti, osservazioni e metadati
- Migliorata la documentazione della struttura dati in `ARCHITECTURE.md`

### Fisso
- Riorganizzazione del dataset JSON per garantire la compatibilità tra `dataset.json` e l'oggetto `DATA` in `index.html`
- Aggiunta voce di changelog mancante per la versione 1.3
- Aggiunti campi root-level `births`, `fertility`, `population` al dataset per allineamento con `DATA`

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
