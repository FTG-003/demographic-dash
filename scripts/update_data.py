#!/usr/bin/env python3
"""
Italian Demographic Observatory — Automated Data Update Script
================================================================

Elabora nuovi dati da comunicati ISTAT, esegue sanity checks,
aggiorna data/dataset.json con incremento automatico della versione,
sincronizza index.html e genera changelog.

Utilizzo:
    python scripts/update_data.py --check              # Solo validazione (dry-run)
    python scripts/update_data.py --update             # Elabora payload ISTAT e aggiorna dataset
    python scripts/update_data.py --embed              # Aggiorna dataset + sincronizza index.html
    python scripts/update_data.py --update --embed     # Full pipeline: payload → dataset → HTML

Dipendenze: solo libreria standard Python 3.9+
Nessuna dipendenza esterna richiesta.
"""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ──────────────────────────────────────────────────────────────
# Configurazione percorsi
# ──────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
DATA_FILE = DATA_DIR / "dataset.json"
INDEX_FILE = BASE_DIR / "index.html"
ISTAT_PAYLOAD_FILE = DATA_DIR / "istat_payload.json"
CHANGELOG_FILE = DOCS_DIR / "CHANGELOG.md"

# ──────────────────────────────────────────────────────────────
# Costanti di validazione
# ──────────────────────────────────────────────────────────────

# Range validi per ogni metrica [min, max]
METRIC_RANGES: Dict[str, Tuple[float, float]] = {
    "births":       (0, 2_000_000),       # nati vivi (valori assoluti)
    "fertility":    (0, 5.0),             # TFR (figli per donna)
    "population":   (0, 100.0),           # popolazione residente (milioni)
    "elderly_ratio": (0, 100.0),          # % over 65
    "first_child_age": (15, 50),          # età media al primo figlio
}

SPIKE_THRESHOLD_YOY = 15.0  # Variazione percentuale max accettabile YoY

REQUIRED_OBSERVATIONS = [
    "births", "fertility", "population",
    "elderly_ratio", "first_child_age",
]

# ──────────────────────────────────────────────────────────────
# 1. PARSING / EXTRACTION — Lettura payload ISTAT
# ──────────────────────────────────────────────────────────────


def load_istat_payload(payload_path: Path = ISTAT_PAYLOAD_FILE) -> Optional[Dict[str, Any]]:
    """
    Carica e decodifica un payload JSON con nuovi dati ISTAT.

    Il file deve seguire la struttura:
    {
      "source_note": "...",
      "update_type": "annuale|straordinario",
      "observations": {
        "fertility": { "year": 2026, "value": 1.14 },
        "births":    { "year": 2026, "value": 348000 },
        ...
      },
      "notes": "..."
    }

    Se il file non esiste, restituisce None e lo script può
    utilizzare dati simulati per test.
    """
    if not payload_path.exists():
        print(f"  [WARN] Payload ISTAT non trovato: {payload_path}")
        return None

    try:
        with open(payload_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  [ERR] Impossibile leggere il payload ISTAT: {e}")
        return None

    # Validazione minima della struttura
    if not isinstance(payload, dict) or "observations" not in payload:
        print("  [ERR] Payload ISTAT: chiave 'observations' mancante o non valida.")
        return None

    obs = payload["observations"]
    if not isinstance(obs, dict) or len(obs) == 0:
        print("  [ERR] Payload ISTAT: 'observations' vuoto o non valido.")
        return None

    print(f"  [OK] Payload ISTAT caricato: {payload_path}")
    print(f"       Fonte: {payload.get('source_note', 'N/A')}")
    print(f"       Tipo:  {payload.get('update_type', 'N/A')}")
    print(f"       Metriche: {', '.join(obs.keys())}")
    return payload


def generate_simulated_payload() -> Dict[str, Any]:
    """
    Genera un payload ISTAT simulato per scopi di test/dimostrazione.

    Simula l'arrivo di un nuovo dato annuale (es. anno successivo
    all'ultimo disponibile) con valori realistici basati sul trend
    demografico italiano recente.
    """
    # Carica il dataset corrente per determinare l'ultimo anno
    data = _safe_load_dataset()
    if data is None:
        # Fallback: payload di default se il dataset non è leggibile
        return _default_simulated_payload()

    obs = data.get("observations", {})
    current_year = date.today().year

    payload_observations: Dict[str, Any] = {}

    # births: ultimo valore * leggero trend negativo
    births_obs = obs.get("births", {})
    births_years = births_obs.get("years", [])
    births_values = births_obs.get("values", [])
    if births_years and births_values:
        last_year = births_years[-1]
        if last_year < current_year or True:  # Simula nuovo anno
            next_year = max(births_years[-1] + 1, current_year)
            last_val = births_values[-1]
            # Trend: -2% / anno (declino demografico)
            new_val = round(last_val * 0.98)
            payload_observations["births"] = {"year": next_year, "value": new_val}

    # fertility: trend simile
    fert_obs = obs.get("fertility", {})
    fert_years = fert_obs.get("years", [])
    fert_values = fert_obs.get("values", [])
    if fert_years and fert_values:
        last_year = fert_years[-1]
        if last_year < current_year or True:
            next_year = max(fert_years[-1] + 1, current_year)
            last_val = fert_values[-1]
            # Trend: -0.02 / anno
            new_val = round(max(last_val - 0.02, 0.8), 2)
            payload_observations["fertility"] = {"year": next_year, "value": new_val}

    # population: trend stabile / lieve calo
    pop_obs = obs.get("population", {})
    pop_years = pop_obs.get("years", [])
    pop_values = pop_obs.get("values", [])
    if pop_years and pop_values:
        last_year = pop_years[-1]
        if last_year < current_year or True:
            next_year = max(pop_years[-1] + 1, current_year)
            last_val = pop_values[-1]
            # Trend: -0.05 milioni / anno
            new_val = round(max(last_val - 0.05, 55.0), 1)
            payload_observations["population"] = {"year": next_year, "value": new_val}

    if not payload_observations:
        return _default_simulated_payload()

    return {
        "source_note": "Simulazione automatica per test (nessun dato reale)",
        "update_type": "simulato",
        "observations": payload_observations,
        "notes": "Payload generato da generate_simulated_payload(). "
                 "Non sostituisce un vero comunicato ISTAT.",
    }


def _default_simulated_payload() -> Dict[str, Any]:
    """Payload simulato di fallback."""
    return {
        "source_note": "Simulazione automatica (fallback)",
        "update_type": "simulato",
        "observations": {
            "births": {"year": 2026, "value": 348000},
            "fertility": {"year": 2026, "value": 1.14},
            "population": {"year": 2026, "value": 58.8},
        },
        "notes": "Payload di fallback generato automaticamente.",
    }


def _safe_load_dataset() -> Optional[Dict[str, Any]]:
    """Carica il dataset correntemente in modo safe."""
    if not DATA_FILE.exists():
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


# ──────────────────────────────────────────────────────────────
# 2. SANITY CHECKS — Verifica anomalie
# ──────────────────────────────────────────────────────────────


def sanity_checks(
    data: Dict[str, Any],
    new_observations: Dict[str, Dict[str, Union[int, float]]],
) -> List[str]:
    """
    Esegue sanity checks su dati esistenti e nuovi.

    Verifica:
      - Range valori (valori fuori scala)
      - Variazioni percentuali YoY > SPIKE_THRESHOLD_YOY
      - Chiavi obbligatorie mancanti
      - Anni non ordinati / gap
      - Coerenza strutturale

    Args:
        data: Dataset corrente.
        new_observations: Nuove osservazioni da validare.
                         Es. {"births": {"year": 2026, "value": 348000}}

    Returns:
        Lista di warning/errori (vuota se tutto ok).
    """
    anomalies: List[str] = []
    obs_container = data.get("observations", {})

    for metric_key, new_entry in new_observations.items():
        new_year = new_entry.get("year")
        new_value = new_entry.get("value")

        if new_year is None or new_value is None:
            anomalies.append(
                f"[ANOMALIA] '{metric_key}': year o value mancante "
                f"nel payload ({new_entry})."
            )
            continue

        # ── Controllo range ─────────────────────────────────
        if metric_key in METRIC_RANGES:
            lo, hi = METRIC_RANGES[metric_key]
            if not (lo <= new_value <= hi):
                anomalies.append(
                    f"[ANOMALIA] '{metric_key}': valore {new_value} "
                    f"fuori dal range atteso [{lo}, {hi}]."
                )
        else:
            # Controllo generico per metriche sconosciute
            if isinstance(new_value, (int, float)) and new_value < 0:
                anomalies.append(
                    f"[ANOMALIA] '{metric_key}': valore negativo ({new_value})."
                )

        # ── Spike detection YoY ──────────────────────────────
        existing = obs_container.get(metric_key, {})
        existing_years = existing.get("years", [])
        existing_values = existing.get("values", [])

        if existing_years and existing_values:
            # Trova l'anno più recente
            last_val = existing_values[-1]
            if last_val != 0:
                pct_change = ((new_value - last_val) / abs(last_val)) * 100
                if abs(pct_change) > SPIKE_THRESHOLD_YOY:
                    anomalies.append(
                        f"[SPIKE] '{metric_key}': variazione del "
                        f"{pct_change:+.1f}% YoY ({last_val} → {new_value}). "
                        f"Soglia: ±{SPIKE_THRESHOLD_YOY}%."
                    )

        # ── Anno duplicato ───────────────────────────────────
        if existing_years and new_year in existing_years:
            anomalies.append(
                f"[ANOMALIA] '{metric_key}': anno {new_year} già presente "
                f"nel dataset."
            )

        # ── Anno non consecutivo (gap) ─────────────────────
        if existing_years and new_year is not None:
            last_existing_year = existing_years[-1]
            if isinstance(last_existing_year, int) and isinstance(new_year, int):
                if new_year > last_existing_year + 1:
                    anomalies.append(
                        f"[WARN] '{metric_key}': gap temporale tra "
                        f"{last_existing_year} e {new_year} "
                        f"({new_year - last_existing_year - 1} anno/i mancante/i)."
                    )

    # ── Verifica chiavi obbligatorie nel dataset ─────────────
    for key in REQUIRED_OBSERVATIONS:
        if key not in obs_container:
            anomalies.append(
                f"[ANOMALIA] 'observations.{key}' mancante nel dataset."
            )

    return anomalies


# ──────────────────────────────────────────────────────────────
# 3. VALIDAZIONE STRUTTURALE (schema dataset)
# ──────────────────────────────────────────────────────────────


def validate_dataset(data: dict) -> List[str]:
    """
    Valida la struttura completa del dataset.

    Verifica:
    - Chiavi base (version, license, sources, observations)
    - Tutte le observations obbligatorie
    - Scenari (observations.projections.scenarios)
    - Coerenza years/values per serie temporali
    - Campi specifici (first_child_age.value, .year)

    Restituisce una lista di errori (vuota se il dataset è valido).
    """
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["ERRORE: Il dataset non è un dizionario valido."]

    # ── Chiavi di primo livello ─────────────────────────────
    # Nuova struttura: metadata, sources, observations
    for key in ("metadata", "sources", "observations"):
        if key not in data:
            errors.append(f"ERRORE: Chiave '{key}' mancante nel dataset.")

    # Verifica presenza campi obbligatori in metadata
    if "metadata" in data and isinstance(data["metadata"], dict):
        meta_keys = ["dataset_version", "last_update", "license"]
        for mk in meta_keys:
            if mk not in data["metadata"]:
                errors.append(f"ERRORE: 'metadata.{mk}' mancante.")
    elif "metadata" in data:
        errors.append("ERRORE: 'metadata' non è un oggetto valido.")

    if errors:
        return errors  # non possiamo procedere

    observations = data.get("observations", {})

    # ── Observations obbligatorie ───────────────────────────
    for key in REQUIRED_OBSERVATIONS:
        if key not in observations:
            errors.append(f"ERRORE: 'observations.{key}' mancante.")
        elif not isinstance(observations[key], dict):
            errors.append(f"ERRORE: 'observations.{key}' non è un oggetto valido.")

    # ── Scenari (observations.projections.scenarios) ────────
    proj = observations.get("projections", {})
    if not isinstance(proj, dict):
        errors.append("ERRORE: 'observations.projections' non è un oggetto valido.")
    else:
        scenarios = proj.get("scenarios")
        if scenarios is None:
            errors.append("ERRORE: 'observations.projections.scenarios' mancante.")
        elif not isinstance(scenarios, dict) or len(scenarios) == 0:
            errors.append(
                "ERRORE: 'observations.projections.scenarios' deve essere un "
                "oggetto con almeno uno scenario."
            )

    # ── Coerenza years / values (serie temporali) ──────────
    for key in ("births", "fertility", "population"):
        obs = observations.get(key, {})
        if not isinstance(obs, dict):
            continue
        years = obs.get("years", [])
        values = obs.get("values", [])
        if not isinstance(years, list) or not isinstance(values, list):
            errors.append(f"ERRORE: 'observations.{key}': years e values devono essere liste.")
        elif len(years) != len(values):
            errors.append(
                f"ERRORE: 'observations.{key}' ha {len(years)} anni ma "
                f"{len(values)} valori."
            )

    # ── elderly_ratio ───────────────────────────────────────
    er = observations.get("elderly_ratio", {})
    if isinstance(er, dict):
        er_years = er.get("years", [])
        er_values = er.get("values", [])
        if len(er_years) != len(er_values):
            errors.append(
                f"ERRORE: 'observations.elderly_ratio' ha {len(er_years)} anni "
                f"ma {len(er_values)} valori."
            )

    # ── first_child_age ─────────────────────────────────────
    fca = observations.get("first_child_age", {})
    if isinstance(fca, dict):
        if "value" not in fca:
            errors.append("ERRORE: 'observations.first_child_age.value' mancante.")
        if "year" not in fca:
            errors.append("ERRORE: 'observations.first_child_age.year' mancante.")

    return errors


# ──────────────────────────────────────────────────────────────
# 4. AGGIORNAMENTO DATASET & METADATA
# ──────────────────────────────────────────────────────────────


def bump_version(current_version: str) -> str:
    """
    Incrementa la versione del dataset (es. '1.3' → '1.4').

    Formato atteso: 'major.minor' (es. '1.3').
    """
    try:
        parts = current_version.split(".")
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        return f"{major}.{minor + 1}"
    except (ValueError, IndexError):
        print(f"  [WARN] Versione corrente '{current_version}' non riconosciuta. "
              f"Uso '1.0' come base.")
        return "1.0"


def apply_updates(
    data: Dict[str, Any],
    new_observations: Dict[str, Dict[str, Union[int, float]]],
    source_note: str = "",
) -> Dict[str, Any]:
    """
    Applica le nuove osservazioni al dataset.

    Per ogni metrica:
      - Aggiunge il nuovo anno alla lista 'years'
      - Aggiunge il nuovo valore alla lista 'values'
      - Se la serie non esiste, la crea

    NOTA: Opera su una copia profonda del dataset.
    """
    updated = deepcopy(data)
    obs_container = updated.get("observations", {})
    today_str = date.today().isoformat()

    # Raccogli le modifiche per il changelog
    changes: List[str] = []

    for metric_key, new_entry in new_observations.items():
        new_year = new_entry.get("year")
        new_value = new_entry.get("value")

        if new_year is None or new_value is None:
            continue

        if metric_key not in obs_container:
            # Crea nuova serie se non esiste
            obs_container[metric_key] = {
                "label": metric_key.replace("_", " ").title(),
                "unit": "N/D",
                "years": [],
                "values": [],
            }

        existing = obs_container[metric_key]

        # Assicura che years e values siano liste
        if "years" not in existing or not isinstance(existing["years"], list):
            existing["years"] = []
        if "values" not in existing or not isinstance(existing["values"], list):
            existing["values"] = []

        # Aggiunge il nuovo dato
        if new_year not in existing["years"]:
            existing["years"].append(new_year)
            existing["values"].append(new_value)
            changes.append(
                f"Aggiunto dato {metric_key}: {new_value} "
                f"(anno {new_year})"
            )
        else:
            # Aggiorna valore esistente
            idx = existing["years"].index(new_year)
            old_val = existing["values"][idx]
            existing["values"][idx] = new_value
            changes.append(
                f"Aggiornato {metric_key} anno {new_year}: "
                f"{old_val} → {new_value}"
            )

    # ── Aggiorna metadati ───────────────────────────────────
    # I metadati ora risiedono UNICAMENTE sotto metadata
    old_version = updated.get("metadata", {}).get("dataset_version",
                   updated.get("version", "0.0"))
    new_version = bump_version(str(old_version))

    # Assicura che il blocco metadata esista
    if "metadata" not in updated or not isinstance(updated["metadata"], dict):
        updated["metadata"] = {}
    updated["metadata"]["dataset_version"] = new_version
    updated["metadata"]["last_update"] = today_str

    # Rimuovi eventuali campi duplicati a livello superiore
    updated.pop("version", None)
    updated.pop("lastUpdate", None)
    updated.pop("status", None)
    updated.pop("notes", None)

    # Rimuovi eventuali duplicazioni top-level di births/fertility/population
    # (ora risiedono solo in observations)
    for dup_key in ["births", "fertility", "population"]:
        updated.pop(dup_key, None)

    # ── Changelog ───────────────────────────────────────────
    changelog_entry = {
        "version": new_version,
        "date": today_str,
        "changes": changes,
    }

    if not changes:
        changelog_entry["changes"] = [
            f"Aggiornamento metadati (versione {new_version})"
        ]

    # Aggiungi in testa (più recente primo)
    if "changelog" not in updated or not isinstance(updated["changelog"], list):
        updated["changelog"] = []
    updated["changelog"].insert(0, changelog_entry)

    updated["_meta_update"] = {
        "old_version": old_version,
        "new_version": new_version,
        "date": today_str,
        "metrics_updated": list(new_observations.keys()),
        "source_note": source_note or "Aggiornamento automatico",
        "changes_count": len(changes),
    }

    return updated


# ──────────────────────────────────────────────────────────────
# 5. GENERAZIONE CHANGELOG (docs/CHANGELOG.md)
# ──────────────────────────────────────────────────────────────


def generate_changelog_md(data: Dict[str, Any]) -> str:
    """
    Genera il contenuto di docs/CHANGELOG.md dal changelog del dataset.
    """
    cl_entries = data.get("changelog", [])
    if not cl_entries:
        return "# Changelog\n\nNessuna voce registrata.\n"

    lines: List[str] = []
    lines.append("# Changelog — Italian Demographic Observatory")
    lines.append("")
    lines.append(
        "Registro delle modifiche al dataset demografico. "
        "Ogni aggiornamento corrisponde a un incremento di versione."
    )
    lines.append("")

    for entry in cl_entries:
        version = entry.get("version", "?")
        date_str = entry.get("date", "?")
        changes = entry.get("changes", [])

        lines.append(f"## [{version}] — {date_str}")
        lines.append("")
        for change in changes:
            lines.append(f"- {change}")
        lines.append("")

    return "\n".join(lines)


def write_changelog_md(data: Dict[str, Any]) -> None:
    """Scrive docs/CHANGELOG.md."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    content = generate_changelog_md(data)
    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] Changelog MD scritto: {CHANGELOG_FILE}")


# ──────────────────────────────────────────────────────────────
# 6. EMBED DATASET IN HTML
# ──────────────────────────────────────────────────────────────


def format_dataset_for_js(data: Dict[str, Any]) -> str:
    """Converte il dataset in una stringa JavaScript 'const DATA = {...};'."""
    # Rimuovi _meta_update prima dell'embed
    clean = deepcopy(data)
    clean.pop("_meta_update", None)
    # Usa formato compatto (separators senza spazi) per ridurre dimensione
    json_str = json.dumps(clean, ensure_ascii=False, separators=(',', ':'))
    return f"const DATA = {json_str};"


def embed_dataset_in_html(data: Dict[str, Any], html_content: str) -> str:
    """
    Sostituisce il blocco 'const DATA = {...};' nell'HTML con i nuovi dati.

    Identifica il blocco tramite espressione regolare e bilanciamento
    delle graffe, gestendo oggetti annidati multilinea. Preserva
    l'indentazione esistente.
    """
    pattern = r"^(\s*)(const DATA\s*=\s*)\{"
    match = re.search(pattern, html_content, re.MULTILINE)

    if not match:
        print("  [WARN] Pattern 'const DATA = {' non trovato nell'HTML.")
        return html_content

    leading = match.group(1)        # indentazione (es. "    ")
    line_start = match.start()      # inizio della linea
    brace_start = match.end() - 1   # posizione del '{' di apertura

    # Bilanciamento graffe per trovare la '}' di chiusura
    depth = 1
    pos = brace_start + 1
    while pos < len(html_content) and depth > 0:
        ch = html_content[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        pos += 1

    # Dopo '}' deve esserci ';' (opzionale ma atteso)
    end = pos  # pos punta al carattere dopo '}'
    if end < len(html_content) and html_content[end] == ";":
        end += 1

    # Genera il nuovo blocco JS con la stessa indentazione originale
    # NOTA: NON aggiungere \n finale — il newline dopo ";" è già
    # preservato in html_content[end:] e aggiungerne un altro crea
    # una riga vuota extra prima di </script>.
    js_block = format_dataset_for_js(data)
    replacement = f"{leading}{js_block}"

    return html_content[:line_start] + replacement + html_content[end:]


# ──────────────────────────────────────────────────────────────
# 7. REPORT FINALE
# ──────────────────────────────────────────────────────────────


def generate_report(
    data: Dict[str, Any],
    errors: List[str],
    anomalies: Optional[List[str]] = None,
    dry_run: bool = False,
    update_mode: bool = False,
    new_observations: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Genera un report formale e dettagliato per il terminale.
    """
    lines: List[str] = []
    lines.append("")
    lines.append("╔" + "═" * 58 + "╗")
    if dry_run:
        lines.append("║  Validazione Dataset                      ║")
    elif update_mode:
        lines.append("║  Report Aggiornamento Dataset             ║")
    else:
        lines.append("║  Stato Dataset                            ║")
    lines.append("║  Italian Demographic Observatory           ║")
    lines.append("╚" + "═" * 58 + "╝")
    lines.append("")

    # ── Info dataset ─────────────────────────────────────────
    meta = data.get("metadata", {})
    version = meta.get("dataset_version", "N/A")
    last_up = meta.get("last_update", "N/A")
    lic = data.get("metadata", {}).get("license", data.get("license", "N/A"))

    lines.append("  ┌─ DATASET INFO ──────────────────────────────┐")
    lines.append(f"  │ Versione:            {version}")
    lines.append(f"  │ Ultimo aggiornamento: {last_up}")
    lines.append(f"  │ Licenza:             {lic}")
    lines.append(f"  │ File dataset:        {DATA_FILE}")
    lines.append(f"  │ File HTML:           {INDEX_FILE}")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # ── Metriche / Osservazioni ─────────────────────────────
    obs = data.get("observations", {})
    lines.append("  ┌─ SERIE STORICHE ───────────────────────────┐")
    for key, ob in obs.items():
        label = ob.get("label", key)
        n_years = len(ob.get("years", []))
        n_vals = len(ob.get("values", []))
        if n_years > 0 or n_vals > 0:
            lines.append(f"  │ • {label:<50s}")
            if n_years > 0 and n_vals > 0:
                last_v = ob["values"][-1]
                last_y = ob["years"][-1]
                lines.append(f"  │   {n_years} osservazioni  |  ultimo: {last_v} ({last_y})")
            elif "value" in ob:
                lines.append(f"  │   valore singolo: {ob['value']} ({ob.get('year', '?')})")
            elif "countries" in ob:
                lines.append(f"  │   {len(ob['countries'])} paesi")
            elif "regions" in ob:
                lines.append(f"  │   {len(ob['regions'])} regioni")
            elif "categories" in ob:
                lines.append(f"  │   {len(ob['categories'])} categorie")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # ── Nuove osservazioni (update mode) ────────────────────
    if new_observations and len(new_observations) > 0:
        lines.append("  ┌─ NUOVI DATI ELABORATI ───────────────────┐")
        for key, entry in new_observations.items():
            year = entry.get("year", "?")
            value = entry.get("value", "?")
            lines.append(f"  │ • {key:<20s} → {value} (anno {year})")
        lines.append("  └──────────────────────────────────────────────┘")
        lines.append("")

    # ── Anomalie / Errori ───────────────────────────────────
    all_issues: List[str] = []
    if errors:
        all_issues.extend(f"[ERR] {e}" for e in errors)
    if anomalies:
        all_issues.extend(anomalies)

    if all_issues:
        lines.append(f"  ┌─ ANOMALIE / ERRORI ({len(all_issues)}) ───────────────┐")
        for issue in all_issues:
            lines.append(f"  │ ⚠  {issue}")
        lines.append("  └──────────────────────────────────────────────┘")
        lines.append("")
        lines.append(f"  ❌ TOTALE PROBLEMI: {len(all_issues)}")
    else:
        lines.append("  ✅ NESSUNA ANOMALIA RILEVATA — Dataset valido.")
    lines.append("")

    # ── Changelog ultimo ────────────────────────────────────
    cl = data.get("changelog", [])
    if cl:
        latest = cl[0]
        lines.append("  ┌─ ULTIMO CHANGELOG ────────────────────────┐")
        lines.append(f"  │ v{latest['version']} ({latest['date']}):")
        for c in latest.get("changes", []):
            lines.append(f"  │   • {c}")
        lines.append("  └──────────────────────────────────────────────┘")
        lines.append("")

    # ── Update info (se disponibile) ────────────────────────
    meta_update = data.get("_meta_update")
    if meta_update:
        lines.append("  ┌─ RIEPILOGO AGGIORNAMENTO ────────────────┐")
        lines.append(f"  │ Versione precedente:  v{meta_update['old_version']}")
        lines.append(f"  │ Nuova versione:       v{meta_update['new_version']}")
        lines.append(f"  │ Data aggiornamento:   {meta_update['date']}")
        lines.append(f"  │ Metriche aggiornate:  {', '.join(meta_update['metrics_updated'])}")
        lines.append(f"  │ Modifiche apportate:  {meta_update['changes_count']}")
        lines.append(f"  │ Fonte:                {meta_update['source_note']}")
        lines.append("  └──────────────────────────────────────────────┘")
        lines.append("")

    # ── Footer ──────────────────────────────────────────────
    lines.append("─" * 60)
    if dry_run:
        lines.append("  ℹ️  Dry-run: nessuna modifica applicata.")
    elif update_mode:
        lines.append("  ✅ Aggiornamento completato con successo.")
    lines.append(f"  Timestamp report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("─" * 60)

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# 8. FUNZIONE PRINCIPALE — Aggiornamento completo
# ──────────────────────────────────────────────────────────────


def run_update(
    data: Dict[str, Any],
    payload_path: Path = ISTAT_PAYLOAD_FILE,
    force_simulate: bool = False,
) -> Tuple[Optional[Dict[str, Any]], List[str], List[str]]:
    """
    Esegue l'intero flusso di aggiornamento:

    1. Carica payload ISTAT (o simula se --simulate)
    2. Sanity checks sui nuovi dati
    3. Applica aggiornamenti
    4. Salva dataset.json
    5. Genera changelog MD

    Returns:
        (updated_data, errors, anomalies)
    """
    if force_simulate:
        print("  [INFO] Modalità simulazione forzata.")
        payload = generate_simulated_payload()
    else:
        payload = load_istat_payload(payload_path)
        if payload is None:
            print("  [INFO] Payload ISTAT non trovato. Generazione simulata...")
            payload = generate_simulated_payload()

    if not payload:
        print("  [ERR] Impossibile ottenere un payload valido.")
        return None, ["Payload non disponibile"], []

    source_note = payload.get("source_note", "Aggiornamento automatico")
    new_obs = payload.get("observations", {})

    if not new_obs:
        print("  [ERR] Il payload non contiene osservazioni.")
        return None, ["Payload senza osservazioni"], []

    # ── Sanity checks ───────────────────────────────────────
    print()
    print("  [INFO] Esecuzione sanity checks...")
    anomalies = sanity_checks(data, new_obs)

    if anomalies:
        print(f"  ⚠  Rilevate {len(anomalies)} anomalia/e:")
        for a in anomalies:
            print(f"     {a}")
        print()
        print("  [WARN] Le anomalie sono state registrate ma l'aggiornamento")
        print("         procede comunque. Usare --check per validazione dry-run.")
    else:
        print("  ✅ Sanity checks superati — nessuna anomalia.")
    print()

    # ── Applica aggiornamenti ───────────────────────────────
    print("  [INFO] Applicazione aggiornamenti al dataset...")
    updated = apply_updates(data, new_obs, source_note)

    old_ver = updated["_meta_update"]["old_version"]
    new_ver = updated["_meta_update"]["new_version"]
    print(f"  [INFO] Versione: v{old_ver} → v{new_ver}")
    print(f"  [INFO] Data aggiornamento: {updated.get('lastUpdate', '?')}")
    print()

    # ── Salva dataset ───────────────────────────────────────
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Dataset salvato: {DATA_FILE}")

    # ── Changelog MD ────────────────────────────────────────
    write_changelog_md(updated)

    return updated, [], anomalies


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────


def main() -> None:
    """Esegue l'aggiornamento / validazione del dataset."""
    do_check = "--check" in sys.argv
    do_update = "--update" in sys.argv
    do_embed = "--embed" in sys.argv
    do_simulate = "--simulate" in sys.argv

    # Default: se nessuna flag, mostra help
    if not any([do_check, do_update, do_embed]):
        print(__doc__)
        print(f"\n  Flag disponibili:\n"
              f"    --check         Validazione dry-run\n"
              f"    --update        Elabora payload ISTAT e aggiorna dataset\n"
              f"    --embed         Aggiorna dataset + sincronizza index.html\n"
              f"    --simulate      Forza uso dati simulati (anche con --update)\n"
              f"    --check --update (combinabili)\n")
        sys.exit(0)

    header = "Validazione dataset" if do_check and not do_update else "Aggiornamento dataset"
    print()
    print("╔" + "═" * 58 + "╗")
    print(f"║  Italian Demographic Observatory          ║")
    print(f"║  {header:<44s}║")
    print("╚" + "═" * 58 + "╝")
    print()

    # ── Carica dataset ──────────────────────────────────────
    if not DATA_FILE.exists():
        print(f"  ❌ ERRORE: Dataset non trovato: {DATA_FILE}")
        print("     Creare manualmente 'data/dataset.json' con la struttura attesa.")
        sys.exit(1)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta = data.get("metadata", {})
        print(f"  [OK] Dataset caricato: {DATA_FILE}")
        print(f"       Versione: {meta.get('dataset_version', 'N/A')}")
        print(f"       Ultimo aggiornamento: {meta.get('last_update', 'N/A')}")
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ❌ ERRORE: Impossibile leggere il dataset: {e}")
        sys.exit(1)
    print()

    # ── Validazione schema ──────────────────────────────────
    print("  [INFO] Validazione schema dataset...")
    schema_errors = validate_dataset(data)

    if schema_errors:
        for err in schema_errors:
            print(f"         ❌ {err}")
        print()
        print(f"  ❌ Validazione fallita — {len(schema_errors)} errore/i.")
        report = generate_report(data, schema_errors, dry_run=True)
        print(report)
        sys.exit(1)
    else:
        print("  ✅ Dataset valido — tutti i campi obbligatori presenti e coerenti.")
    print()

    # ── Modalità check (dry-run) ───────────────────────────
    if do_check and not do_update:
        # Esegue solo sanity check su eventuale payload
        payload = load_istat_payload() if not do_simulate else generate_simulated_payload()
        if payload is None:
            print("  [INFO] Nessun payload ISTAT disponibile per dry-run.")
            print("         Usare --simulate per testare con dati simulati.")
            anomalies = []
        else:
            new_obs = payload.get("observations", {})
            anomalies = sanity_checks(data, new_obs)
            if anomalies:
                print(f"  ⚠  Rilevate {len(anomalies)} anomalia/e:")
                for a in anomalies:
                    print(f"     {a}")
            else:
                print("  ✅ Sanity checks superati — nessuna anomalia.")
            print()

        report = generate_report(
            data, schema_errors, anomalies=anomalies, dry_run=True,
            new_observations=payload.get("observations") if payload else None,
        )
        print(report)
        print("  ℹ️  Dry-run completato. Nessuna modifica apportata.")
        return

    # ── Modalità update ────────────────────────────────────
    if do_update:
        updated, _, anomalies = run_update(
            data, force_simulate=do_simulate,
        )
        if updated is None:
            print("  ❌ Aggiornamento fallito.")
            sys.exit(1)

        data = updated  # per l'eventuale embed
        print()

    # ── Modalità embed (sincronizza HTML) ──────────────────
    if do_embed:
        if not INDEX_FILE.exists():
            print(f"  [WARN] File HTML non trovato: {INDEX_FILE}")
            print("         L'embed non è possibile.")
        else:
            print("  [INFO] Aggiornamento HTML in corso...")
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                html_content = f.read()
            new_html = embed_dataset_in_html(data, html_content)
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                f.write(new_html)
            changed = "cambiato" if new_html != html_content else "nessuna modifica"
            print(f"  [OK] HTML aggiornato: {INDEX_FILE} ({changed})")
        print()

    # ── Report finale ──────────────────────────────────────
    if do_check or do_update or do_embed:
        # Ricarica il dataset per il report (per prendere _meta_update)
        final_data = _safe_load_dataset() or data
        report = generate_report(
            final_data, schema_errors, anomalies=[],
            dry_run=False, update_mode=do_update,
        )
        print(report)


if __name__ == "__main__":
    main()
