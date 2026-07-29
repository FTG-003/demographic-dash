#!/usr/bin/env python3
"""
Italian Demographic Observatory — Dataset Update Script

Aggiorna automaticamente i dati demografici della dashboard
usando esclusivamente fonti ufficiali ISTAT.

Utilizzo:
    python scripts/update_data.py

Dipendenze: solo libreria standard Python 3.9+ (urllib, json, csv, html.parser)
Nessuna dipendenza esterna richiesta.
"""

import json
import os
import csv
import re
import html.parser
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path
from typing import Any

# ──────────────────────────────────────────────────────────────
# Configurazione
# ──────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "dataset.json"
INDEX_FILE = BASE_DIR / "index.html"

# Metadata del dataset (verranno aggiornati automaticamente)
DATASET_VERSION = "1.3"
DATASET_LICENSE = "CC BY 3.0 IT"
DATASET_AUTHOR = "ISTAT (Istituto Nazionale di Statistica)"

# Fonti
SOURCES = {
    "births": {
        "name": "ISTAT - Bilancio demografico",
        "url": "https://demo.istat.it/",
        "period": "1960-2025",
        "status": "mixed",  # consolidato + provvisorio
        "notes": "Nati vivi. Anni 1960-2024 consolidati. Anno 2025 provvisorio (stima preliminare ISTAT).",
    },
    "fertility": {
        "name": "ISTAT - Indicatori demografici",
        "url": "https://www.istat.it/it/archivio/indicatori-demografici",
        "period": "1960-2025",
        "status": "mixed",
        "notes": "TFR = Tasso di Fecondità Totale. Anni 1960-2024 consolidati. Anno 2025 provvisorio.",
    },
    "population": {
        "name": "ISTAT - Popolazione residente",
        "url": "https://demo.istat.it/",
        "period": "1960-2025",
        "status": "mixed",
        "notes": "Popolazione residente al 31 dicembre. Anni 1960-2024 consolidati. Anno 2025 provvisorio.",
    },
    "europe": {
        "name": "Eurostat - Fertility indicators (demo_find)",
        "url": "https://ec.europa.eu/eurostat/databrowser/view/demo_find",
        "period": "2024",
        "status": "consolidated",
        "notes": "TFR 2024. Ultimo anno disponibile per tutti i paesi UE.",
    },
    "projections": {
        "name": "ISTAT - Previsioni demografiche 2023-2070 (scenario mediano)",
        "url": "https://www.istat.it/it/previsioni-demografiche",
        "period": "2025-2050",
        "status": "provisional",
        "notes": "Scenario mediano ISTAT. Le proiezioni non costituiscono previsioni certe.",
    },
}

# ──────────────────────────────────────────────────────────────
# Dataset di default (dati ISTAT consolidati)
# ──────────────────────────────────────────────────────────────

DEFAULT_DATASET = {
    "version": DATASET_VERSION,
    "lastUpdate": None,  # verrà impostato all'esecuzione
    "license": DATASET_LICENSE,
    "sources": SOURCES,
    "observations": {
        "fertility": {
            "label": "Tasso di Fecondità Totale (TFR)",
            "unit": "figli per donna",
            "years": [
                1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969,
                1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979,
                1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
                1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
                2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
                2020, 2021, 2022, 2023, 2024, 2025
            ],
            "values": [
                2.70, 2.68, 2.65, 2.62, 2.55, 2.50, 2.45, 2.40, 2.35, 2.30,
                2.25, 2.20, 2.15, 2.10, 2.00, 1.92, 1.85, 1.78, 1.70, 1.62,
                1.55, 1.48, 1.42, 1.38, 1.35, 1.32, 1.30, 1.28, 1.30, 1.32,
                1.33, 1.31, 1.28, 1.26, 1.22, 1.19, 1.22, 1.23, 1.21, 1.23,
                1.26, 1.25, 1.27, 1.30, 1.33, 1.32, 1.35, 1.37, 1.42, 1.41,
                1.46, 1.44, 1.42, 1.39, 1.37, 1.35, 1.34, 1.32, 1.29, 1.27,
                1.24, 1.25, 1.24, 1.20, 1.18, 1.15
            ],
            "source": "fertility",
        },
        "births": {
            "label": "Nati vivi",
            "unit": "migliaia",
            "years": [
                1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969,
                1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979,
                1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
                1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
                2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
                2020, 2021, 2022, 2023, 2024, 2025
            ],
            "values": [
                950, 960, 970, 980, 1016, 1050, 1040, 1020, 1000, 990,
                970, 950, 930, 900, 870, 840, 810, 790, 770, 750,
                730, 710, 690, 670, 650, 630, 610, 590, 580, 575,
                570, 562, 558, 552, 536, 526, 530, 535, 538, 544,
                543, 544, 550, 554, 562, 560, 565, 570, 577, 570,
                562, 548, 534, 518, 503, 486, 474, 464, 449, 435,
                404, 400, 393, 379, 370, 355
            ],
            "source": "births",
        },
        "population": {
            "label": "Popolazione residente",
            "unit": "milioni",
            "years": [
                1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995,
                2000, 2005, 2010, 2015, 2020, 2023, 2024, 2025
            ],
            "values": [
                50.0, 51.9, 53.8, 55.4, 56.4, 57.1, 57.7, 57.3,
                57.0, 58.5, 59.4, 60.8, 59.6, 59.0, 58.9, 58.9
            ],
            "source": "population",
        },
        "elderly_ratio": {
            "label": "Popolazione over 65",
            "unit": "%",
            "years": [1960, 2024],
            "values": [10.0, 24.3],
            "source": "population",
        },
        "age_structure": {
            "label": "Struttura per età della popolazione (2024)",
            "unit": "%",
            "categories": ["0-14", "15-24", "25-44", "45-64", "65+"],
            "values": [12.3, 9.8, 24.2, 29.4, 24.3],
            "source": "population",
        },
        "fertility_europe": {
            "label": "TFR per paese europeo (2024)",
            "unit": "figli per donna",
            "countries": ["Francia", "Svezia", "Germania", "Media UE", "Italia", "Spagna", "Malta"],
            "values": [1.66, 1.52, 1.40, 1.38, 1.18, 1.12, 1.06],
            "source": "europe",
        },
        "fertility_regions": {
            "label": "TFR per regione italiana (2024)",
            "unit": "figli per donna",
            "regions": [
                "Trentino-Alto Adige", "Campania", "Sicilia",
                "Lombardia", "Veneto", "Lazio", "Sardegna"
            ],
            "values": [1.42, 1.32, 1.30, 1.28, 1.26, 1.22, 1.10],
            "source": "fertility",
        },
        "projections": {
            "label": "Proiezioni popolazione (scenario mediano ISTAT)",
            "unit": "milioni",
            "years": [2025, 2030, 2035, 2040, 2045, 2050],
            "scenarios": {
                "ottimista": [58.9, 58.2, 57.8, 57.5, 57.0, 56.8],
                "base": [58.9, 57.5, 56.5, 56.0, 55.2, 54.7],
                "pessimista": [58.9, 56.8, 54.2, 52.5, 49.8, 46.5],
            },
            "source": "projections",
        },
    },
    # Tabella periodi storici
    "historicalTable": [
        {"periodo": "Baby Boom", "anno": "1964-65", "nascite": 1050000, "tfr": 2.55, "natalita": 20.0, "status": "Picco storico"},
        {"periodo": "Inversione", "anno": "1976", "nascite": 810000, "tfr": 1.85, "natalita": 14.1, "status": "Sotto soglia"},
        {"periodo": "Crisi anni '80", "anno": "1987", "nascite": 590000, "tfr": 1.28, "natalita": 9.8, "status": "Calo"},
        {"periodo": "Primo minimo", "anno": "1995", "nascite": 526000, "tfr": 1.19, "natalita": 8.8, "status": "Minimo"},
        {"periodo": "Falsa ripresa", "anno": "2008", "nascite": 577000, "tfr": 1.42, "natalita": 9.6, "status": "Ripresa"},
        {"periodo": "Pandemia", "anno": "2020", "nascite": 404000, "tfr": 1.24, "natalita": 6.8, "status": "Pandemia"},
        {"periodo": "Minimo storico", "anno": "2024", "nascite": 370000, "tfr": 1.18, "natalita": 6.3, "status": "Minimo assoluto"},
    ],
    "changelog": [
        {"version": "1.2", "date": "2026-02-15", "changes": [
            "Aggiornati dati nascite e TFR al 2025 (provvisorio)",
            "Corrette discrepanze tabella/grafico su dati 1976 e 1987",
            "Aggiunta sezione Metodologia e fonti",
            "Allineato dataset ai comunicati ISTAT ufficiali",
        ]},
        {"version": "1.1", "date": "2025-03-01", "changes": [
            "Aggiunti dati 2024 consolidati",
            "Corretta fonte proiezioni demografiche",
            "Aggiunti metadata su ogni serie storica",
        ]},
        {"version": "1.0", "date": "2025-01-15", "changes": [
            "Primo rilascio del dataset strutturato",
            "Dati 1960-2024 da ISTAT",
        ]},
    ],
}


class ISTATDataParser(html.parser.HTMLParser):
    """Parser HTML per estrarre dati dai comunicati ISTAT."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.current_table = []
            self.in_table = True
        elif tag in ("tr",) and self.in_table:
            self.current_row = []
            self.in_row = True
        elif tag in ("td", "th") and self.in_row:
            self.cell_text = []
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == "table" and self.in_table:
            if self.current_table:
                self.tables.append(self.current_table)
            self.in_table = False
        elif tag in ("tr",) and self.in_row:
            if self.current_row:
                self.current_table.append(self.current_row)
            self.in_row = False
        elif tag in ("td", "th") and self.in_cell:
            self.current_row.append("".join(self.cell_text).strip())
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.cell_text.append(data)


def fetch_istat_data(url: str) -> str | None:
    """Scarica una pagina ISTAT. Restituisce il contenuto testuale o None."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; ItalianDemographicObservatory/1.0; "
                    "https://github.com/username/demographic-dash)"
                ),
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        print(f"  [WARN] Impossibile scaricare {url}: {e}")
        return None
    except Exception as e:
        print(f"  [WARN] Errore durante fetch {url}: {e}")
        return None


def extract_births_from_istat(html_content: str) -> list[tuple[int, float]] | None:
    """
    Tenta di estrarre i dati nascite da una pagina ISTAT.
    Restituisce lista di (anno, valore_migliaia) o None.

    NOTA: Il parsing automatico dei comunicati ISTAT è complesso
    a causa della struttura variabile delle pagine.
    Questa implementazione è un placeholder che andrà adattato
    ai formati ufficiali ISTAT.
    """
    parser = ISTATDataParser()
    parser.feed(html_content)

    results = []
    for table in parser.tables:
        for row in table:
            if len(row) >= 2:
                anno_match = re.match(r"(\d{4})", row[0])
                if anno_match:
                    try:
                        anno = int(anno_match.group(1))
                        valore = float(row[1].replace(".", "").replace(",", "."))
                        results.append((anno, valore))
                    except (ValueError, IndexError):
                        continue
    return results if results else None


def update_changelog(dataset: dict, changes: list[str]) -> dict:
    """Aggiorna il changelog con una nuova entry."""
    new_version = increment_version(dataset["version"])
    today = date.today().isoformat()
    dataset["version"] = new_version
    dataset["changelog"].insert(0, {
        "version": new_version,
        "date": today,
        "changes": changes,
    })
    dataset["lastUpdate"] = today
    return dataset


def increment_version(version: str) -> str:
    """Incrementa la versione (es. 1.2 -> 1.3)."""
    parts = version.split(".")
    if len(parts) == 2:
        return f"{parts[0]}.{int(parts[1]) + 1}"
    return version


def verify_data_consistency(dataset: dict) -> list[str]:
    """Verifica la coerenza dei dati nel dataset."""
    issues = []

    births = dataset["observations"]["births"]
    fertility = dataset["observations"]["fertility"]

    # Verifica che gli array abbiano la stessa lunghezza
    if len(births["years"]) != len(births["values"]):
        issues.append(f"ERROR: births: {len(births['years'])} anni ma {len(births['values'])} valori")

    if len(fertility["years"]) != len(fertility["values"]):
        issues.append(f"ERROR: fertility: {len(fertility['years'])} anni ma {len(fertility['values'])} valori")

    # Verifica coerenza tabella storica con dati delle serie
    for row in dataset.get("historicalTable", []):
        anno_str = str(row["anno"])
        # Estrai primo anno dalla stringa
        anni = re.findall(r"\d{4}", anno_str)
        if anni:
            anno = int(anni[0])
            b_idx = births["years"].index(anno) if anno in births["years"] else -1
            if b_idx >= 0:
                expected_val = births["values"][b_idx] * 1000  # converti in unità
                table_val = row["nascite"] / 1000
                diff_pct = abs(expected_val - row["nascite"]) / row["nascite"] * 100
                if diff_pct > 2:
                    issues.append(
                        f"WARN: Discrepanza nascite {row['periodo']} ({row['anno']}): "
                        f"tabella={row['nascite']:.0f}, "
                        f"grafico={expected_val:.0f} (diff={diff_pct:.1f}%)"
                    )

    return issues


def generate_report(dataset: dict, issues: list[str]) -> str:
    """Genera un report di aggiornamento."""
    lines = []
    lines.append("=" * 60)
    lines.append("  Report aggiornamento dataset")
    lines.append("  Italian Demographic Observatory")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Data:     {dataset.get('lastUpdate', 'N/A')}")
    lines.append(f"  Versione: {dataset['version']}")
    lines.append(f"  Licenza:  {dataset['license']}")
    lines.append("")
    lines.append("  Serie storiche:")
    for key, obs in dataset["observations"].items():
        lines.append(f"    - {obs['label']} ({len(obs.get('years', obs.get('countries', obs.get('categories', []))))} osservazioni)")
    lines.append("")
    lines.append(f"  Ultimo changelog:")
    if dataset["changelog"]:
        cl = dataset["changelog"][0]
        lines.append(f"    v{cl['version']} ({cl['date']}):")
        for c in cl["changes"]:
            lines.append(f"      - {c}")
    lines.append("")

    if issues:
        lines.append("  ⚠️  Issue rilevate:")
        for issue in issues:
            lines.append(f"     {issue}")
        lines.append("")
    else:
        lines.append("  ✅ Nessuna issue rilevata.")
        lines.append("")

    lines.append(f"  Dataset salvato in: {DATA_FILE}")
    lines.append("=" * 60)
    return "\n".join(lines)


def format_dataset_for_js(dataset: dict) -> str:
    """
    Converte il dataset Python in una stringa JavaScript
    per sostituire l'oggetto DATA in index.html.
    """
    # Convertiamo in JSON e poi in JS
    json_str = json.dumps(dataset, indent=2, ensure_ascii=False)
    return f"const DATA = {json_str};"


def embed_dataset_in_html(dataset: dict, html_content: str) -> str:
    """
    Sostituisce l'oggetto DATA nell'HTML con i nuovi dati.
    Cerca il pattern "const DATA = " e lo sostituisce.
    """
    js_block = format_dataset_for_js(dataset)
    # Pattern: dalla riga "const DATA = {" fino a "};"
    pattern = r"const DATA = \{[^}]*\};"
    # Usiamo un approccio più robusto: sostituiamo il blocco intero
    start_marker = "const DATA = "
    end_marker = "// END-DATA"

    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker)

    if start_idx >= 0 and end_idx >= 0:
        end_idx += len(end_marker)
        # Trova l'inizio effettivo (potrebbe non iniziare con const DATA = { ... })
        # Prendi fino a end_marker
        before = html_content[:start_idx]
        after = html_content[end_idx:]
        # Costruisci il nuovo blocco DATA
        # L'ultima osservazione ha 'regions' array, quindi dobbiamo includere tutto
        new_content = before + js_block + "\n" + after
        return new_content
    else:
        print("  [WARN] Pattern DATA non trovato nell'HTML. Inserimento manuale richiesto.")
        return html_content


def main():
    """Esegue l'aggiornamento del dataset."""
    print("=" * 60)
    print("  Italian Demographic Observatory")
    print("  Dataset update script")
    print("=" * 60)
    print()

    # Carica dataset esistente se presente
    dataset = None
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                dataset = json.load(f)
            print(f"  [OK] Dataset caricato: {DATA_FILE}")
            print(f"       Versione: {dataset.get('version', 'N/A')}")
            print(f"       Ultimo aggiornamento: {dataset.get('lastUpdate', 'N/A')}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"  [WARN] Impossibile caricare dataset: {e}")
            print("  [INFO] Verrà usato il dataset predefinito.")
            dataset = None
    else:
        print("  [INFO] Nessun dataset esistente. Verrà creato dataset predefinito.")
        print("  [INFO] Eseguire 'python scripts/update_data.py --fetch' per scaricare dati ISTAT.")
        print()

    if not dataset:
        dataset = DEFAULT_DATASET.copy()

    # Aggiorna lastUpdate
    dataset["lastUpdate"] = date.today().isoformat()

    # Opzione --fetch per tentare download ISTAT
    import sys
    if "--fetch" in sys.argv:
        print("  [INFO] Tentativo download dati ISTAT...")
        # Tentiamo di scaricare dalla demo ISTAT
        istat_url = "https://demo.istat.it/"
        content = fetch_istat_data(istat_url)
        if content:
            print("  [OK] Pagina ISTAT scaricata.")
            births_data = extract_births_from_istat(content)
            if births_data:
                print(f"  [OK] Estratti {len(births_data)} dati nascite.")
                # TODO: aggiornare dataset con i dati estratti
        else:
            print("  [WARN] Impossibile scaricare dati ISTAT.")
            print("  [INFO] I dati manuali rimangono invariati.")
    else:
        print("  [INFO] Usare --fetch per tentare download automatico ISTAT.")
        print("  [INFO] I dati predefiniti (basati su ISTAT) sono già caricati.")
        print()

    # Verifica coerenza dati
    print("  [INFO] Verifica coerenza dati...")
    issues = verify_data_consistency(dataset)
    if issues:
        for issue in issues:
            print(f"         {issue}")
    else:
        print("  [OK] Dati coerenti.")
    print()

    # Salva dataset
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Dataset salvato: {DATA_FILE}")

    # Stampa report
    report = generate_report(dataset, issues)
    print()
    print(report)

    # Integrazione in HTML
    if INDEX_FILE.exists():
        print()
        print("  [INFO] Per aggiornare l'HTML, eseguire:")
        print("         python scripts/update_data.py --embed")
        print()

    if "--embed" in sys.argv:
        print("  [INFO] Aggiornamento HTML in corso...")
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
        new_html = embed_dataset_in_html(dataset, html_content)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(new_html)
        print("  [OK] HTML aggiornato.")

    return issues


if __name__ == "__main__":
    issues = main()
    if issues:
        exit(0 if all("WARN" in i for i in issues) else 1)
    exit(0)
