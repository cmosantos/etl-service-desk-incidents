import pandas as pd

REQUIRED_COLS = ["ticket_id", "created_at", "resolved_at", "priority", "title", "description"]

def extract_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")
    return df
