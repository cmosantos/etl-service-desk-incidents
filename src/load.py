from pathlib import Path
from sqlalchemy import create_engine

def save_parquet(df, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

def save_sqlite(df, db_path: str, table="incidents"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql(table, engine, if_exists="replace", index=False)

def save_reports(aggs, md_path: str):
    out_dir = Path(md_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = ["# ETL Report\n"]
    for name, table in aggs.items():
        csv_path = out_dir / f"{name}.csv"
        table.to_csv(csv_path, index=False)
        lines.append(f"## {name}\n")
        lines.append(table.head(20).to_markdown(index=False))
        lines.append("\n")

    Path(md_path).write_text("\n".join(lines), encoding="utf-8")
