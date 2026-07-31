# Data Sources — Italian Demographic Observatory

> Documento metodologico completo sulle fonti dati impiegate nell'Osservatorio Demografico Italiano. Ogni serie storica è tracciata con fonte, periodo, stato di consolidamento e licenza.

---

## 1. Quadro sinottico delle fonti

| # | Dataset | Fonte | Periodo | Ultimo agg. | Stato | Licenza |
|---|---|---|---|---|---|---|
| 1 | **Nascite (nati vivi)** | ISTAT — Bilancio demografico | 1960–2025 | 2026-02 | ✅ Consolidato 1960–2024 / ⚠️ Provvisorio 2025 | CC BY 3.0 IT |
| 2 | **TFR (Tasso di Fecondità Totale)** | ISTAT — Indicatori demografici | 1960–2025 | 2026-02 | ✅ Consolidato 1960–2024 / ⚠️ Provvisorio 2025 | CC BY 3.0 IT |
| 3 | **Popolazione residente** | ISTAT — Popolazione residente | 1960–2025 | 2026-02 | ✅ Consolidato 1960–2024 / ⚠️ Provvisorio 2025 | CC BY 3.0 IT |
| 4 | **Struttura per età** | ISTAT — Popolazione residente per età | 2025 | 2026-02 | ⚠️ Provvisorio (stima 2025) | CC BY 3.0 IT |
| 5 | **Decessi annuali** | ISTAT — Mortalità | 1960–2025 | 2026-02 | ✅ Consolidato 1960–2024 / ⚠️ Provvisorio 2025 | CC BY 3.0 IT |
| 6 | **TFR regionale** | ISTAT — Indicatori regionali | 2024 | 2026-02 | ✅ Consolidato | CC BY 3.0 IT |
| 7 | **TFR paesi europei** | Eurostat — Fertility indicators (demo_find) | 2024 | 2025-12 | ✅ Consolidato | CC BY 4.0 |
| 8 | **Proiezioni demografiche** | ISTAT — Previsioni demografiche 2023–2070 | 2025–2050 | 2025-09 | 🔮 Previsionale (scenario mediano) | CC BY 3.0 IT |
| 9 | **Età media al primo figlio** | ISTAT — Indicatori demografici | 2024 | 2026-02 | ✅ Consolidato | CC BY 3.0 IT |
| 10 | **Rapporto di dipendenza anziani** | ISTAT — Popolazione residente per età | 1960 / 2024–2025 | 2026-02 | ✅ Consolidato 1960,2024 / ⚠️ Provv. 2025 | CC BY 3.0 IT |
| 11 | **Over 65 ratio** | ISTAT — Indicatori demografici | 1960–2025 | 2026-02 | ✅ Consolidato 1960,2024 / ⚠️ Provv. 2025 | CC BY 3.0 IT |

> **Legenda stato dei dati:**
> - ✅ **Consolidato** = dato definitivo pubblicato dall'istituto statistico, non soggetto a revisione
> - ⚠️ **Provvisorio** = stima preliminare basata su dati parziali, suscettibile di revisione
> - 🔮 **Previsionale** = proiezione statistica basata su modelli demografici, non costituisce previsione certa

---

## 2. Dettaglio metodologico per fonte

### 2.1 ISTAT — Bilancio demografico (nascite)

| Campo | Dettaglio |
|---|---|
| **Fonte** | ISTAT — Rilevazione degli iscritti in anagrafe per nascita |
| **Serie** | Nati vivi (valori assoluti) |
| **Periodo** | 1960–2025 |
| **Unità** | Valori assoluti (il dataset li esprime in migliaia) |
| **Frequenza** | Annuale |
| **URL** | [demo.istat.it](https://demo.istat.it/) |
| **Metodo** | Rilevazione totale (censuaria) degli eventi di nascita registrati nelle anagrafi comunali. I dati 1960–2025 sono consolidati; il dato 2026 è una stima parziale (primo semestre). |
| **Licenza** | [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) |

### 2.2 ISTAT — Indicatori demografici (TFR)

| Campo | Dettaglio |
|---|---|
| **Fonte** | ISTAT — Indicatori demografici (Tavola: Tasso di fecondità totale per anno) |
| **Serie** | TFR — Tasso di Fecondità Totale (numero medio di figli per donna in età fertile 15–49 anni) |
| **Periodo** | 1960–2025 |
| **Unità** | Figli per donna |
| **Frequenza** | Annuale |
| **URL** | [istat.it/it/archivio/indicatori-demografici](https://www.istat.it/it/archivio/indicatori-demografici) |
| **Metodo** | Il TFR è calcolato come somma dei tassi di fecondità specifici per età (fx) su tutte le età tra 15 e 49 anni, moltiplicato per l'ampiezza della classe (1 anno). Formula: `TFR = Σ fx` per x da 15 a 49. |
| **Licenza** | [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) |

### 2.3 ISTAT — Popolazione residente

| Campo | Dettaglio |
|---|---|
| **Fonte** | ISTAT — Popolazione residente (bilancio demografico) |
| **Serie** | Popolazione residente al 31 dicembre |
| **Periodo** | 1960–2025 (con cadenza quinquennale 1960–2000, annuale da 2000) |
| **Unità** | Milioni di residenti |
| **Frequenza** | Annuale |
| **URL** | [demo.istat.it](https://demo.istat.it/) |
| **Metodo** | Popolazione residente in Italia (iscritti in anagrafe). Include cittadini italiani e stranieri regolarmente iscritti. Esclude i temporaneamente presenti. |
| **Licenza** | [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) |

### 2.4 ISTAT — Dati 2025 (status consolidato)

| Dato | Valore 2025 | Stato | Note |
|---|---|---|---|
| **Nascite** | 355.000 | ✅ **Consolidato** | Dato definitivo ISTAT da bilancio demografico. |
| **TFR** | 1,14 figli/donna | ✅ **Consolidato** | Dato definitivo ISTAT da indicatori demografici. |
| **Popolazione** | 58,94 milioni | ✅ **Consolidato** | Dato definitivo ISTAT popolazione residente. |
| **Over 65** | 24,7% | ✅ **Consolidato** | Composizione per età definitiva. |
| **Età media** | 46,8 anni | ✅ **Consolidato** | Età mediana della popolazione. |

### 2.5 ISTAT — Previsioni demografiche 2023–2070

| Campo | Dettaglio |
|---|---|
| **Fonte** | ISTAT — Previsioni della popolazione residente 2023–2070 |
| **Serie** | Scenario mediano (base), scenario ottimista (alta fecondità + alta immigrazione), scenario pessimista (bassa fecondità + bassa immigrazione) |
| **Periodo** | 2025–2050 (selezionato) |
| **Unità** | Milioni di residenti |
| **Frequenza** | Quinquennale |
| **URL** | [istat.it/it/previsioni-demografiche](https://www.istat.it/it/previsioni-demografiche) |
| **Metodo** | Modello multistato per componenti (Cohort-Component Method). Le ipotesi dello scenario base: TFR gradualmente crescente da 1.20 a 1.45 nel 2070; saldo migratorio netto positivo ma decrescente; speranza di vita in aumento. |
| **Licenza** | [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) |
| **Nota** | Le proiezioni non costituiscono previsioni certe, ma scenari ipotetici basati su assunzioni demografiche coerenti. |

### 2.6 ISTAT — Mortalità (decessi)

| Campo | Dettaglio |
|---|---|
| **Fonte** | ISTAT — Mortalità (bilancio demografico) |
| **Serie** | Decessi annuali |
| **Periodo** | 1960–2025 |
| **Unità** | Migliaia |
| **Frequenza** | Annuale |
| **URL** | [demo.istat.it](https://demo.istat.it/) |
| **Metodo** | Rilevazione totale degli eventi di morte registrati nelle anagrafi comunali. I dati 1960–2025 sono consolidati; il dato 2026 è parziale (stima primo semestre). |
| **Licenza** | [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) |

### 2.7 Eurostat — Fertility indicators (demo_find)

| Campo | Dettaglio |
|---|---|
| **Fonte** | Eurostat — Fertility indicators (dataset: demo_find) |
| **Serie** | TFR per paese europeo |
| **Periodo** | 2024 (ultimo anno consolidato disponibile) |
| **Unità** | Figli per donna |
| **Frequenza** | Annuale |
| **URL** | [ec.europa.eu/eurostat/databrowser/view/demo_find](https://ec.europa.eu/eurostat/databrowser/view/demo_find) |
| **Metodo** | Dati armonizzati raccolti presso gli istituti statistici nazionali secondo il regolamento UE 1260/2013. Il TFR è calcolato con metodologia Eurostat standard. |
| **Licenza** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

---

## 3. Classificazione dello stato dei dati

Il dataset interno classifica ogni serie storica con uno dei seguenti stati:

| Stato | Descrizione | Codice dataset | Azioni consentite |
|---|---|---|---|
| **Consolidato** | Dato definitivo pubblicato, non soggetto a revisione | `"consolidated"` | Pubblicazione, analisi, benchmark |
| **Provvisorio** | Stima preliminare basata su dati parziali | `"provisional"` | Pubblicazione con avvertenza, non utilizzabile per benchmark definitivi |
| **Misto** | Serie che contiene sia dati consolidati che provvisori | `"mixed"` | Pubblicazione con indicazione del periodo |
| **Previsionale** | Proiezione statistica basata su modelli | `"provisional"` (proiezioni) | Pubblicazione come scenario, non come previsione |

### Mappa dello stato per serie

| Serie | Anni consolidati | Anni provvisori | Anni previsionali |
|---|---|---|---|
| `births` | 1960–2024 | 2025 | — |
| `fertility` | 1960–2024 | 2025 | — |
| `population` | 1960–2024 | 2025 | — |
| `elderly_ratio` | 1960, 2024 | 2025 | — |
| `first_child_age` | 2024 | — | — |
| `age_structure` | — | 2025 | — |
| `fertility_europe` | 2024 | — | — |
| `fertility_regions` | 2024 | — | — |
| `deaths` | 1960–2024 | 2025 | — |
| `projections` | — | — | 2025–2050 |

---

## 4. Metadati interni del dataset

Ogni serie storica nell'oggetto `DATA` contiene i seguenti metadati strutturati:

```json
{
  "births": {
    "label": "Nati vivi",
    "unit": "migliaia",
    "years": [1960, 1961, …, 2025],
    "values": [1035, 1018, …, 355],
    "source": "births",
    "metadata": {
      "source": "ISTAT - Bilancio demografico",
      "sourceUrl": "https://demo.istat.it/",
      "period": "1960-2025",
      "lastUpdate": "2026-02-15",
      "status": "mixed",
      "notes": "Nati vivi. Anni 1960-2025 consolidati. Anno 2026 parziale.",
      "version": "1.6"
    }
  }
}
```

I metadati di fonte sono centralizzati nell'oggetto `DATA.sources`:

```json
{
  "sources": {
    "births": {
      "name": "ISTAT - Bilancio demografico",
      "url": "https://demo.istat.it/",
      "period": "1960-2025",
      "status": "mixed",
      "notes": "Nati vivi. Anni 1960-2025 consolidati. Anno 2026 parziale."
    }
  }
}
```

---

## 5. Frequenza di aggiornamento

| Fonte | Cadenza aggiornamento | Tempo tipico di rilascio |
|---|---|---|
| ISTAT — Bilancio demografico | Annuale | Febbraio (dato anno precedente provvisorio) → Novembre (revisione consolidata) |
| ISTAT — Indicatori demografici | Annuale | Febbraio |
| ISTAT — Popolazione residente | Annuale | Aprile |
| ISTAT — Previsioni demografiche | Ogni 3–5 anni | 2023 (ultimo rilascio), prossimo atteso 2027–2028 |
| Eurostat — Fertility indicators | Annuale | Dicembre (dato anno precedente) |

---

## 6. Collegamenti diretti alle fonti

| Risorsa | URL |
|---|---|
| ISTAT — Bilancio demografico (serie storiche) | [https://demo.istat.it/](https://demo.istat.it/) |
| ISTAT — Indicatori demografici | [https://www.istat.it/it/archivio/indicatori-demografici](https://www.istat.it/it/archivio/indicatori-demografici) |
| ISTAT — Popolazione residente | [https://demo.istat.it/](https://demo.istat.it/) |
| ISTAT — Previsioni demografiche 2023–2070 | [https://www.istat.it/it/previsioni-demografiche](https://www.istat.it/it/previsioni-demografiche) |
| ISTAT — Indicatori regionali | [https://www.istat.it/it/archivio/indicatori-territoriali](https://www.istat.it/it/archivio/indicatori-territoriali) |
| Eurostat — Fertility statistics | [https://ec.europa.eu/eurostat/statistics-explained/](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Fertility_statistics) |
| Eurostat — demo_find dataset | [https://ec.europa.eu/eurostat/databrowser/view/demo_find](https://ec.europa.eu/eurostat/databrowser/view/demo_find) |

---

## 7. Limitazioni e avvertenze

1. **Dati 2026 parziali:** i dati relativi all'anno 2026 sono stime parziali ANPR (primo semestre) suscettibili di revisione. Il dato consolidato sarà disponibile a fine 2027.
2. **Proiezioni 2025–2050:** gli scenari previsionali sono basati su modelli statistici e non costituiscono previsioni certe. Lo scenario "base" rappresenta l'ipotesi centrale ISTAT.
3. **Dati regionali 2024:** il confronto regionale si basa sull'ultimo anno consolidato disponibile (2024).
4. **Confronto europeo 2024:** il confronto TFR tra paesi UE si basa sull'anno 2024 (ultimo anno consolidato disponibile per tutti i paesi).
5. **Popolazione:** i dati di popolazione sono espressi in milioni di residenti al 31 dicembre. La serie storica ha cadenza quinquennale fino al 2000, poi annuale.

---

## 8. Licenza dei dati

- **Dati ISTAT:** [CC BY 3.0 IT](https://creativecommons.org/licenses/by/3.0/it/) — *Attribuzione 3.0 Italia*
  - È consentito condividere e adattare i dati per qualsiasi scopo, anche commerciale, con l'obbligo di attribuire la fonte.
  - Attribuzione raccomandata: *"Fonte: ISTAT — Bilancio demografico / Indicatori demografici"*

- **Dati Eurostat:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — *Creative Commons Attribution 4.0 International*
  - Attribuzione raccomandata: *"Fonte: Eurostat — demo_find"*

- **Codice del progetto:** Licenza MIT (vedi LICENSE).

---

> **Documento manutenuto come parte del repository.**  
> Ultimo aggiornamento: 2026-07-31 — Versione v1.6.
