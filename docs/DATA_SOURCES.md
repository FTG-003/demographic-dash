# Fonti dei dati

## Italian Demographic Observatory

### Dataset demografici

| Dataset | Fonte | Periodo | Ultimo aggiornamento | Stato | Licenza |
|---|---|---|---|---|---|
| Nascite (1960-2025) | ISTAT - Bilancio demografico | 1960-2025 | 2026-02 | Consolidato 1960-2024, Provvisorio 2025 | CC BY 3.0 IT |
| Tasso di fecondità totale (TFR) | ISTAT - Indicatori demografici | 1960-2025 | 2026-02 | Consolidato 1960-2024, Provvisorio 2025 | CC BY 3.0 IT |
| Popolazione residente | ISTAT - Popolazione residente | 1960-2025 | 2026-02 | Consolidato 1960-2024, Provvisorio 2025 | CC BY 3.0 IT |
| Struttura per età | ISTAT - Popolazione residente per età | 2024 | 2026-02 | Consolidato | CC BY 3.0 IT |
| TFR regionale | ISTAT - Indicatori regionali | 2024 | 2026-02 | Consolidato | CC BY 3.0 IT |
| TFR paesi europei | Eurostat - Fertility indicators | 2024 | 2025-12 | Consolidato | CC BY 4.0 |
| Proiezioni demografiche | ISTAT - Previsioni demografiche 2023-2070 | 2025-2050 | 2025-09 | Provvisorio | CC BY 3.0 IT |

### Collegamenti alle fonti

- **ISTAT - Bilancio demografico**: https://www.istat.it/it/archivio/bilancio-demografico
- **ISTAT - Indicatori demografici**: https://www.istat.it/it/archivio/indicatori-demografici
- **ISTAT - Popolazione residente**: https://demo.istat.it/
- **ISTAT - Previsioni demografiche**: https://www.istat.it/it/previsioni-demografiche
- **Eurostat - Fertility**: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Fertility_statistics

### Metadata dataset

Il dataset interno `DATA` contiene per ogni serie storica:

- `source`: nome della fonte
- `sourceUrl`: URL di riferimento
- `period`: periodo coperto
- `lastUpdate`: data ultimo aggiornamento
- `status`: consolidato | provvisorio | stimato
- `notes`: note aggiuntive
- `version`: versione del dataset

### Definizioni

- **TFR (Tasso di Fecondità Totale)**: numero medio di figli per donna in età fertile (15-49 anni) in un dato anno.
- **Soglia di sostituzione**: TFR di 2,1 figli per donna, livello necessario per mantenere stabile la popolazione in assenza di migrazioni.
- **Natalità**: rapporto tra il numero di nati vivi e la popolazione media, espresso per mille (‰).
- **Popolazione residente**: popolazione registrata in anagrafe, inclusi gli italiani residenti all'estero solo se iscritti all'AIRE.

### Limitazioni

- I dati del 2025 sono provvisori e basati su stime ISTAT preliminari.
- Le proiezioni 2025-2050 sono basate sullo scenario centrale ISTAT e non costituiscono previsioni certe.
- I dati regionali si riferiscono al 2024 (ultimo dato consolidato disponibile).
