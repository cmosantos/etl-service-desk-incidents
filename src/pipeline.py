import argparse
from src.extract import extract_csv
from src.transform import transform, agg_counts, agg_breach_rate_by_priority
from src.load import save_clean_csv, save_sqlite, save_report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/raw/incidents.csv")
    p.add_argument("--clean_csv", default="data/processed/incidents_clean.csv")
    p.add_argument("--db", default="outputs/db/incidents.sqlite")
    p.add_argument("--report", default="outputs/reports/summary.md")
    args = p.parse_args()

    rows = extract_csv(args.input)
    clean_rows, metrics = transform(rows)

    by_category = agg_counts(clean_rows, "category_pred")
    by_priority = agg_counts(clean_rows, "priority")
    breach_rate = agg_breach_rate_by_priority(clean_rows)

    save_clean_csv(clean_rows, args.clean_csv)
    save_sqlite(clean_rows, args.db)
    save_report(args.report, metrics, by_category, by_priority, breach_rate)

    print("OK pipeline:", metrics)
    print("Report:", args.report)

if __name__ == "__main__":
    main()
