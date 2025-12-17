from __future__ import annotations
from datetime import datetime

SLA_MINUTES = {"P1": 60, "P2": 120, "P3": 240, "P4": 480}

# Classificação por palavras-chave (sem ML, sem libs)
RULES = [
    ("M365",  ["outlook", "teams", "exchange", "defender", "microsoft 365", "m365"]),
    ("Rede",  ["vpn", "switch", "latência", "latencia", "perda de pacote", "link intermitente", "roteador", "router"]),
    ("Acesso",["senha", "mfa", "perm", "permiss", "bloqueado", "conta desabilitada", "login falhando"]),
    ("Backup",["backup", "restore", "veeam", "job falhou", "storage"]),
]

def _parse_iso(dt: str) -> datetime:
    # suporta ISO "YYYY-MM-DDTHH:MM:SS"
    return datetime.fromisoformat(dt)

def classify_text(text: str) -> str:
    t = (text or "").lower()
    for label, keywords in RULES:
        if any(k in t for k in keywords):
            return label
    return "Servidor"

def transform(rows: list[dict]) -> tuple[list[dict], dict]:
    seen = set()
    out = []
    dropped = 0

    for row in rows:
        tid = (row.get("ticket_id") or "").strip()
        if not tid:
            dropped += 1
            continue
        # dedupe
        if tid in seen:
            continue
        seen.add(tid)

        created = _parse_iso(row["created_at"])
        resolved = _parse_iso(row["resolved_at"])
        resolution_minutes = int((resolved - created).total_seconds() // 60)

        priority = (row.get("priority") or "P3").strip()
        sla = SLA_MINUTES.get(priority, 240)
        is_breach = resolution_minutes > sla

        text = f'{row.get("title","")} {row.get("description","")}'.lower()
        category_pred = classify_text(text)

        enriched = dict(row)
        enriched["resolution_minutes"] = resolution_minutes
        enriched["sla_minutes"] = sla
        enriched["is_sla_breach"] = int(is_breach)  # 0/1 para sqlite
        enriched["dow"] = created.strftime("%A")
        enriched["hour"] = created.hour
        enriched["category_pred"] = category_pred

        out.append(enriched)

    metrics = {"rows_in": len(rows), "rows_out": len(out), "dropped": dropped}
    return out, metrics

def agg_counts(rows: list[dict], key: str) -> list[tuple[str, int]]:
    counts = {}
    for r in rows:
        k = str(r.get(key, ""))
        counts[k] = counts.get(k, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

def agg_breach_rate_by_priority(rows: list[dict]) -> list[tuple[str, float]]:
    tot = {}
    br = {}
    for r in rows:
        p = str(r.get("priority", ""))
        tot[p] = tot.get(p, 0) + 1
        br[p] = br.get(p, 0) + int(r.get("is_sla_breach", 0))
    out = []
    for p in sorted(tot.keys()):
        out.append((p, (br[p] / tot[p]) if tot[p] else 0.0))
    return out
