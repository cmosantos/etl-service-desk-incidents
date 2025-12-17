import argparse
from src.extract import extract_csv
from src.transform import transform, build_aggregations
from src.load import save_parquet, save_sqlite, save_reports

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/raw/incidents.csv")
    p.add_argument("--parquet", default="data/processed/incidents_clean.parquet")
    p.add_argument("--db", default="outputs/db/incidents.sqlite")
    p.add_argument("--report", default="outputs/reports/summary.md")
    args = p.parse_args()

    df = extract_csv(args.input)
    df_clean, metrics = transform(df)
    aggs = build_aggregations(df_clean)

    save_parquet(df_clean, args.parquet)
    save_sqlite(df_clean, args.db)
    save_reports(aggs, args.report)

    print("OK pipeline:", metrics)

if __name__ == "__main__":
    main()
