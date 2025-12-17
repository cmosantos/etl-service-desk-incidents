import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

SLA_MINUTES = {"P1": 60, "P2": 120, "P3": 240, "P4": 480}

def _prep(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["created_at"] = pd.to_datetime(out["created_at"], errors="coerce")
    out["resolved_at"] = pd.to_datetime(out["resolved_at"], errors="coerce")
    out = out.dropna(subset=["ticket_id", "created_at", "resolved_at"])

    out["title"] = out["title"].astype(str).str.strip()
    out["description"] = out["description"].astype(str).str.strip()
    out["text"] = (out["title"] + " " + out["description"]).str.lower()

    out = out.drop_duplicates(subset=["ticket_id"], keep="last")

    out["resolution_minutes"] = (out["resolved_at"] - out["created_at"]).dt.total_seconds() / 60
    out["dow"] = out["created_at"].dt.day_name()
    out["hour"] = out["created_at"].dt.hour
    out["sla_minutes"] = out["priority"].map(SLA_MINUTES).fillna(240)
    out["is_sla_breach"] = out["resolution_minutes"] > out["sla_minutes"]
    return out

def classify_category(df: pd.DataFrame):
    out = df.copy()
    metrics = {"model_trained": False}

    if "category" not in out.columns:
        out["category_pred"] = "Unknown"
        return out, metrics

    X = out["text"].fillna("")
    y = out["category"].astype(str)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(min_df=2, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=200)),
    ])

    pipe.fit(Xtr, ytr)
    acc = pipe.score(Xte, yte)

    out["category_pred"] = pipe.predict(X)
    metrics.update({"model_trained": True, "accuracy": float(acc)})
    return out, metrics

def transform(df: pd.DataFrame):
    clean = _prep(df)
    return classify_category(clean)

def build_aggregations(df: pd.DataFrame):
    return {
        "by_category": df.groupby("category_pred").size().sort_values(ascending=False).reset_index(name="count"),
        "by_priority": df.groupby("priority").size().sort_values(ascending=False).reset_index(name="count"),
        "sla_breach_rate": df.groupby("priority")["is_sla_breach"].mean().reset_index().rename(columns={"is_sla_breach": "breach_rate"}),
    }
