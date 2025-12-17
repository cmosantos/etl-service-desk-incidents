import csv
import sqlite3
from pathlib import Path

def save_clean_csv(rows: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def save_sqlite(rows: list[dict], db_path: str, table: str = "incidents") -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return

    cols = list(rows[0].keys())
    col_names = ",".join([f'"{c}"' for c in cols])
    placeholders = ",".join(["?"] * len(cols))
    col_sql = ",".join([f'"{c}" TEXT' for c in cols])

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS "{table}"')
    cur.execute(f'CREATE TABLE "{table}" ({col_sql})')

    insert_sql = f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})'
    data = [[str(r.get(c, "")) for c in cols] for r in rows]
    cur.executemany(insert_sql, data)

    conn.commit()
    conn.close()

def save_report(md_path: str, metrics: dict, by_category, by_priority, breach_rate) -> None:
    Path(md_path).parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# ETL Report\n")
    lines.append(f"- Rows in: **{metrics.get('rows_in')}**")
    lines.append(f"- Rows out: **{metrics.get('rows_out')}**")
    lines.append(f"- Dropped: **{metrics.get('dropped')}**\n")

    def table(title, header, rows):
        lines.append(f"## {title}\n")
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for r in rows:
            lines.append("| " + " | ".join(r) + " |")
        lines.append("")

    table("By Category (Pred)", ["category_pred", "count"], [[k, str(v)] for k, v in by_category])
    table("By Priority", ["priority", "count"], [[k, str(v)] for k, v in by_priority])
    table("SLA Breach Rate", ["priority", "breach_rate"], [[p, f"{rate:.2%}"] for p, rate in breach_rate])

    Path(md_path).write_text("\n".join(lines), encoding="utf-8")
