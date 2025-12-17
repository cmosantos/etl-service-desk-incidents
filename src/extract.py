import csv

REQUIRED_COLS = ["ticket_id", "created_at", "resolved_at", "priority", "title", "description"]

def extract_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)

    missing = [c for c in REQUIRED_COLS if c not in (rows[0].keys() if rows else [])]
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")

    return rows
