#!/usr/bin/env python3
"""
Italian Demographic Observatory — Dataset Update Script

Aggiorna automaticamente i dati demografici della dashboard
usando come unica fonte di verità data/dataset.json.

Utilizzo:
    python scripts/update_data.py              # aggiorna dataset
    python scripts/update_data.py --embed       # aggiorna dataset + index.html
    python scripts/update_data.py --check       # solo validazione (dry-run)

Dipendenze: solo libreria standard Python 3.9+
Nessuna dipendenza esterna richiesta.
"""

import json
import re
import sys
from pathlib import Path
from datetime import date

# ──────────────────────────────────────────────────────────────
# Configurazione
# ──────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "dataset.json"
INDEX_FILE = BASE_DIR / "index.html"

# ──────────────────────────────────────────────────────────────
# Validazione schema dataset
# ──────────────────────────────────────────────────────────────

REQUIRED_OBSERVATIONS = [
    "births",
    "fertility",
    "population",
    "elderly_ratio",
    "first_child_age",
]
SCENARIOS_PATH = ("projections", "scenarios")  # observations.projections.scenarios


def validate_dataset(data: dict) -> list[str]:
    """
    Valida la struttura del dataset.

    Verifica:
    - Chiavi base (version, license, sources, observations)
    - Tutte le observations obbligatorie
    - Scenari (observations.projections.scenarios)
    - Coerenza years/values per serie temporali
    - Campi specifici (first_child_age.value, .year)

    Restituisce una lista di errori (vuota se il dataset è valido).
    """
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["ERRORE: Il dataset non è un dizionario valido."]

    # ── Chiavi di primo livello ─────────────────────────────
    for key in ("version", "license", "sources", "observations"):
        if key not in data:
            errors.append(f"ERRORE: Chiave '{key}' mancante nel dataset.")

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
# Generazione report
# ──────────────────────────────────────────────────────────────


def generate_report(data: dict, errors: list[str], dry_run: bool = False) -> str:
    """Genera un report di aggiornamento / validazione."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(
        f"  {'Validazione dataset' if dry_run else 'Report aggiornamento dataset'}"
    )
    lines.append("  Italian Demographic Observatory")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Versione: {data.get('version', 'N/A')}")
    lines.append(f"  Data:     {data.get('lastUpdate', 'N/A')}")
    lines.append(f"  Licenza:  {data.get('license', 'N/A')}")
    lines.append("")
    lines.append("  Serie storiche:")

    for key, obs in data.get("observations", {}).items():
        label = obs.get("label", key)
        # Conta il numero di osservazioni in modo adattivo
        count_keys = ("years", "countries", "regions", "categories")
        n = None
        for ck in count_keys:
            val = obs.get(ck)
            if isinstance(val, list):
                n = len(val)
                break
        # Valore singolo (es. first_child_age)
        if n is None and "value" in obs:
            n = "1 valore"
        elif n is not None:
            n = f"{n} osservazioni"
        else:
            n = ""

        if n:
            lines.append(f"    - {label} ({n})")
        else:
            lines.append(f"    - {label}")

    lines.append("")

    if errors:
        lines.append(f"  ❌ {len(errors)} errore/i rilevato/i:")
        for err in errors:
            lines.append(f"     {err}")
        lines.append("")
    else:
        lines.append("  ✅ Dataset valido — nessun errore.")
        lines.append("")

    if data.get("changelog"):
        cl = data["changelog"][0]
        lines.append("  Ultimo changelog:")
        lines.append(f"    v{cl['version']} ({cl['date']}):")
        for c in cl["changes"]:
            lines.append(f"      - {c}")
        lines.append("")

    lines.append(f"  Dataset: {DATA_FILE}")
    if not dry_run:
        lines.append(f"  HTML:    {INDEX_FILE}")
    lines.append("=" * 60)
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Embed dataset in HTML
# ──────────────────────────────────────────────────────────────


def format_dataset_for_js(data: dict) -> str:
    """Converte il dataset in una stringa JavaScript 'const DATA = {...};'."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    return f"const DATA = {json_str};"


def embed_dataset_in_html(data: dict, html_content: str) -> str:
    """
    Sostituisce il blocco 'const DATA = {...};' nell'HTML con i nuovi dati.

    Identifica il blocco tramite espressione regolare e bilanciamento
    delle graffe, gestendo oggetti annidati multilinea. Preserva
    l'indentazione esistente e aggiorna automaticamente i metadati
    (versione, lastUpdate) inclusi nel dataset passato.
    """
    pattern = r"^(\s*)(const DATA\s*=\s*)\{"
    match = re.search(pattern, html_content, re.MULTILINE)

    if not match:
        print("  [WARN] Pattern 'const DATA = {' non trovato nell'HTML.")
        return html_content

    leading = match.group(1)       # indentazione (es. "    ")
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
    js_block = format_dataset_for_js(data)
    replacement = f"{leading}{js_block}\n"

    return html_content[:line_start] + replacement + html_content[end:]


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────


def main() -> None:
    """Esegue l'aggiornamento / validazione del dataset."""
    dry_run = "--check" in sys.argv
    do_embed = "--embed" in sys.argv

    header = "Validazione dataset" if dry_run else "Aggiornamento dataset"
    print("=" * 60)
    print(f"  Italian Demographic Observatory")
    print(f"  {header}")
    print("=" * 60)
    print()

    # ── Carica dataset (UNICA fonte di verità) ──────────────
    if not DATA_FILE.exists():
        print(f"  ❌ ERRORE: Dataset non trovato: {DATA_FILE}")
        print("     Creare manualmente 'data/dataset.json' con la struttura attesa.")
        sys.exit(1)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  [OK] Dataset caricato: {DATA_FILE}")
        print(f"       Versione: {data.get('version', 'N/A')}")
        print(f"       Ultimo aggiornamento: {data.get('lastUpdate', 'N/A')}")
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ❌ ERRORE: Impossibile leggere il dataset: {e}")
        sys.exit(1)

    print()

    # ── Validazione schema ──────────────────────────────────
    print("  [INFO] Validazione schema dataset...")
    errors = validate_dataset(data)

    if errors:
        for err in errors:
            print(f"         {err}")
        print()
        print(f"  ❌ Validazione fallita — {len(errors)} errore/i.")
        print()
        report = generate_report(data, errors, dry_run=True)
        print(report)
        sys.exit(1)
    else:
        print("  ✅ Dataset valido — tutti i campi obbligatori presenti e coerenti.")
    print()

    # ── Dry-run (--check) ───────────────────────────────────
    if dry_run:
        report = generate_report(data, errors, dry_run=True)
        print(report)
        print("  ℹ️  Dry-run completato. Nessuna modifica apportata.")
        return

    # ── Aggiorna metadati ───────────────────────────────────
    today = date.today().isoformat()
    data["lastUpdate"] = today
    print(f"  [INFO] Metadata aggiornati: lastUpdate = {today}")

    # ── Salva dataset ──────────────────────────────────────
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Dataset salvato: {DATA_FILE}")

    # ── Integrazione in HTML ───────────────────────────────
    if do_embed and INDEX_FILE.exists():
        print()
        print("  [INFO] Aggiornamento HTML in corso...")
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
        new_html = embed_dataset_in_html(data, html_content)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  [OK] HTML aggiornato: {INDEX_FILE}")
    elif do_embed and not INDEX_FILE.exists():
        print(f"  [WARN] File HTML non trovato: {INDEX_FILE}")
    else:
        print()
        print("  [INFO] Per aggiornare anche l'HTML, eseguire:")
        print("         python scripts/update_data.py --embed")
        print()

    # ── Report finale ──────────────────────────────────────
    print()
    report = generate_report(data, errors)
    print(report)


if __name__ == "__main__":
    main()
