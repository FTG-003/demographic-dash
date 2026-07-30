# Method — Italian Demographic Observatory

> Documento tecnico-scientifico che illustra la metodologia alla base degli indicatori demografici visualizzati nella dashboard. Ogni indicatore è definito con formula, interpretazione, fonte e contesto.

---

## Indice

1. [TFR — Tasso di Fecondità Totale](#1-tfr--tasso-di-fecondità-totale)
2. [Soglia di sostituzione (2,1)](#2-soglia-di-sostituzione-21)
3. [Natalità](#3-natalità)
4. [Rapporto di Dipendenza degli Anziani](#4-rapporto-di-dipendenza-degli-anziani)
5. [Età media al primo figlio](#5-età-media-al-primo-figlio)
6. [Popolazione residente](#6-popolazione-residente)
7. [Metodologia dei 3 scenari previsionali ISTAT](#7-metodologia-dei-3-scenari-previsionali-istat)
8. [Riferimenti](#8-riferimenti)

---

## 1. TFR — Tasso di Fecondità Totale

### Definizione

Il **Tasso di Fecondità Totale (TFR)** è il numero medio di figli che una donna avrebbe durante la sua vita fertile (15–49 anni) se, nell'anno considerato, fosse esposta ai tassi di fecondità specifici per età osservati in quell'anno.

### Formula

```
TFR = Σ (fx × n)   per x da 15 a 49
```

dove:
- `fx` = tasso di fecondità specifico per l'età `x` (numero di nati vivi da donne di età `x` / popolazione femminile media di età `x`)
- `n` = ampiezza della classe di età (tipicamente 1 anno)

Poiché le classi sono annuali (`n = 1`), la formula si semplifica in:

```
TFR = Σ fx   per x da 15 a 49
```

### Interpretazione

| TFR | Significato |
|---|---|
| **> 2,1** | Popolazione in crescita (sostituzione garantita) |
| **= 2,1** | Popolazione stabile (soglia di sostituzione) |
| **1,5 – 2,0** | Moderatamente sotto sostituzione |
| **< 1,5** | Fortemente sotto sostituzione |
| **< 1,3** | Declino demografico accelerato (lowest-low fertility) |

### Valori attuali

- **Italia 2024 (consolidato):** 1,18 figli per donna — minimo storico assoluto
- **Italia 2025 (provvisorio):** 1,15 figli per donna (stima preliminare ISTAT)
- **Media UE 2024:** 1,38 figli per donna (dato Eurostat)
- **Soglia di sostituzione:** 2,1 figli per donna

### Fonte

ISTAT — Indicatori demografici, Tavola "Tasso di fecondità totale per anno".  
Anni 1960–2024 consolidati. Anno 2025 provvisorio (stima preliminare).

---

## 2. Soglia di sostituzione (2,1)

### Definizione

La **soglia di sostituzione** (o *replacement level*) è il livello di TFR necessario affinché una generazione di donne riesca esattamente a "sostituire" sé stessa nella generazione successiva, in assenza di migrazioni.

### Perché 2,1 e non 2,0?

Il valore teorico è 2,0 (due genitori → due figli). Tuttavia, nella pratica si usa **2,1** per tenere conto di:

1. **Mortalità infantile e pre-riproduttiva** — non tutti i nati raggiungono l'età fertile
2. **Rapporto di mascolinità alla nascita** — nascono circa 105 maschi ogni 100 femmine; servono più nascite totali per garantire 1 donna in età fertile
3. **Sterilità primaria** — una frazione della popolazione femminile non ha figli per ragioni biologiche

### Rappresentazione nella dashboard

La soglia di 2,1 è rappresentata come **linea orizzontale tratteggiata** nel grafico principale della serie storica TFR (1950–2025), visualizzata tramite `chartjs-plugin-annotation`. L'Italia è scesa sotto questa soglia nel **1976** e non vi ha più fatto ritorno.

---

## 3. Natalità

### Definizione

Il **tasso di natalità** (o *crude birth rate*) è il rapporto tra il numero di nati vivi in un anno e la popolazione media dello stesso anno, espresso per mille (‰).

### Formula

```
Natalità (‰) = (Nati vivi / Popolazione media) × 1000
```

### Interpretazione

| Natalità (‰) | Livello |
|---|---|
| > 30‰ | Molto alto |
| 20–30‰ | Alto |
| 15–20‰ | Moderato |
| 10–15‰ | Basso |
| < 10‰ | Molto basso |

### Valori nella serie storica

| Anno | Nascite | Natalità (‰) |
|---|---|---|
| 1964 (Record Baby Boom) | 1.035.207 | ~20,0‰ |
| 1965 (Secondo picco) | 1.018.000 | ~19,6‰ |
| 1976 | 810.000 | ~14,1‰ |
| 1995 (primo minimo) | 526.000 | ~8,8‰ |
| 2024 (minimo assoluto) | 370.000 | ~6,3‰ |

> **Nota storica:** Il record assoluto del baby boom italiano è il **1964** con 1.035.207 nati (TFR 2,55), superando il 1965 che registrò 1.018.000 nati (TFR 2,50).

---

## 4. Rapporto di Dipendenza degli Anziani

### Definizione

Il **Rapporto di Dipendenza degli Anziani** (*Old-Age Dependency Ratio*) misura il carico potenziale sulla popolazione in età lavorativa esercitato dalla popolazione anziana (65+ anni).

### Formula

```
Rapporto Dipendenza Anziani (%) = (Popolazione 65+ / Popolazione 15–64) × 100
```

### Interpretazione

| Valore | Significato |
|---|---|
| **10%** (1960) | 1 anziano ogni 10 lavoratori |
| **24,3%** (2024) | ~1 anziano ogni 4 lavoratori |
| **> 30%** (proiezione 2035) | Più di 1 anziano ogni 3 lavoratori |

### Trend

L'Italia presenta uno dei rapporti di dipendenza anziani più alti dell'Unione Europea, conseguenza combinata del bassissimo TFR prolungato (dal 1976) e dell'aumento della speranza di vita.

| Anno | Over 65 | Rapporto dipendenza |
|---|---|---|
| **1960** | 10,0% | ~1 anziano ogni 10 lavoratori |
| **2024** | 24,3% | ~1 anziano ogni 4 lavoratori |
| **2025 (provv.)** | **24,7%** | **14,8 milioni** di over 65 |
| **2035 (proiez.)** | >30% | Più di 1 anziano ogni 3 lavoratori |

ISTAT — Popolazione residente per età. Anni 1960 (consolidato) e 2024 (consolidato).

---

## 5. Età media al primo figlio

### Definizione

L'**età media della donna al parto per il primo figlio** è l'indicatore del rinvio della maternità. Si calcola come:

```
Età media primo figlio = Σ (x × N₁x) / Σ N₁x
```

dove:
- `x` = età della donna
- `N₁x` = numero di primi nati da donne di età `x`

### Valori attuali

| Paese | Età media primo figlio | Anno |
|---|---|---|
| **Italia** | **31,8 anni** | 2024 |
| Media UE | ~29,5 anni | 2023 |
| Spagna | ~31,6 anni | 2023 |
| Germania | ~30,2 anni | 2023 |

L'Italia detiene il **record UE** per l'età media più alta al primo figlio (31,8 anni), fattore che contribuisce significativamente al basso TFR (più tardi si ha il primo figlio, meno tempo rimane per eventuali figli successivi).

### Fonte

ISTAT — Indicatori demografici, Tavola "Età media al parto". Dato 2024 consolidato.

---

## 6. Popolazione residente

### Definizione

La **popolazione residente** è costituita dalle persone iscritte nelle anagrafi della popolazione residente dei comuni italiani, aventi dimora abituale nel territorio nazionale.

### Serie storica

| Anno | Popolazione (milioni) | Variazione |
|---|---|---|
| 1960 | 50,0 | — |
| 1990 | 57,7 | +7,7M in 30 anni |
| 2015 | 60,8 | Picco storico |
| 2020 | 59,6 | Calo (-1,2M in 5 anni) |
| 2024 | 58,9 | -1,9M dal picco 2015 |
| 2025 | 58,9 (provv.) | Stazionario |

### Fonte

ISTAT — Popolazione residente (bilancio demografico). Anni 1960–2025.

---

## 7. Metodologia dei 3 scenari previsionali ISTAT

### 7.1 Premessa

Le proiezioni demografiche non sono previsioni, ma **scenari ipotetici** costruiti su un insieme coerente di assunzioni riguardanti fecondità, mortalità e migrazioni. ISTAT pubblica periodicamente le "Previsioni della popolazione residente" utilizzando un modello multistato per componenti (*Cohort-Component Method*).

### 7.2 I tre scenari

| Scenario | TFR (2050) | Saldo migratorio annuo (2050) | Risultato |
|---|---|---|---|
| **Scenario base (mediano)** | 1,35–1,40 | +150.000 | Popolazione 54,7M nel 2050 |
| **Scenario ottimista (alto)** | 1,50–1,55 | +200.000 | Popolazione 56,8M nel 2050 |
| **Scenario pessimista (basso)** | 1,15–1,20 | +80.000 | Popolazione 46,5M nel 2050 |

### 7.3 Modello: Cohort-Component Method

Il modello di proiezione per componenti si basa sull'equazione demografica fondamentale:

```
P(t+1) = P(t) + N(t) - M(t) + I(t) - E(t)
```

dove:
- `P(t)` = popolazione al tempo `t`
- `N(t)` = nati vivi nell'intervallo `t → t+1`
- `M(t)` = morti nell'intervallo `t → t+1`
- `I(t)` = immigrati nell'intervallo `t → t+1`
- `E(t)` = emigrati nell'intervallo `t → t+1`

Il modello applica questa equazione **per sesso e classe di età** (coorte), proiettando anno per anno la popolazione futura sulla base di:

1. **Ipotesi di fecondità:** TFR futuro per scenario, distribuzione dei tassi specifici per età
2. **Ipotesi di mortalità:** tavole di mortalità proiettate con aumento della speranza di vita
3. **Ipotesi migratorie:** saldo migratorio netto annuo per scenario

### 7.4 Limitazioni

- Le proiezioni non incorporano eventi imprevedibili (pandemie, guerre, crisi economiche)
- Il saldo migratorio è la componente più volatile e incerta
- Le ipotesi di fecondità non considerano cambiamenti strutturali nelle preferenze familiari
- Orizzonte considerato: 2025–2050 (la dashboard mostra passi quinquennali)

### 7.5 Visualizzazione nella dashboard

Il grafico "Proiezioni demografiche" mostra tre curve distinte con bande cromatiche:

- **Ottimista (verde):** scenario favorevole
- **Base (blu):** scenario mediano, giudicato più probabile da ISTAT
- **Pessimista (rosso):** scenario sfavorevole

Ogni curva parte dallo stesso dato 2025 (58,9M) e diverge progressivamente.

### 7.6 Fonte

ISTAT — Previsioni della popolazione residente 2023–2070 (pubblicate settembre 2023).  
Periodo estratto: 2025–2050 (passi quinquennali).

---

## 8. Riferimenti

### Fonti primarie

- **ISTAT — Indicatori demografici:** [https://www.istat.it/it/archivio/indicatori-demografici](https://www.istat.it/it/archivio/indicatori-demografici)
- **ISTAT — Bilancio demografico:** [https://demo.istat.it/](https://demo.istat.it/)
- **ISTAT — Previsioni demografiche 2023–2070:** [https://www.istat.it/it/previsioni-demografiche](https://www.istat.it/it/previsioni-demografiche)
- **Eurostat — Fertility indicators:** [https://ec.europa.eu/eurostat/databrowser/view/demo_find](https://ec.europa.eu/eurostat/databrowser/view/demo_find)

### Letteratura di riferimento

- Eurostat (2013). *Demography Report 2013.* Publications Office of the European Union.
- ISTAT (2023). *Previsioni della popolazione residente 2023–2070 — Nota metodologica.*
- Kohler, H.-P., Billari, F.C., & Ortega, J.A. (2002). "The Emergence of Lowest-Low Fertility in Europe During the 1990s." *Population and Development Review*, 28(4), 641–680.

---

> **Documento tecnico manutenuto come parte del repository.**  
> Ultimo aggiornamento: 2026-07-30 — Versione dataset v1.4.
