import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

CATEGORIES = ["Rede", "Servidor", "M365", "Acesso", "Backup"]
PRIORITIES = ["P1", "P2", "P3", "P4"]

TEMPLATES = {
    "Rede": ["VPN caiu", "Switch sem resposta", "Latência alta", "Perda de pacote", "Link intermitente"],
    "Servidor": ["CPU alta", "Disco cheio", "Serviço não inicia", "Reboot inesperado", "VM travada"],
    "M365": ["Outlook não abre", "Teams com erro", "Login falhando", "Exchange com atraso", "Defender alerta"],
    "Acesso": ["Senha expirada", "Usuário bloqueado", "Sem permissão", "MFA falhando", "Conta desabilitada"],
    "Backup": ["Job falhou", "Backup lento", "Restore necessário", "Veeam erro", "Storage sem espaço"],
}

def main(out_path="data/raw/incidents.csv", n=500, seed=42):
    random.seed(seed)
    base = datetime.now() - timedelta(days=30)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for i in range(1, n + 1):
        cat = random.choice(CATEGORIES)
        pri = random.choice(PRIORITIES)

        created = base + timedelta(minutes=random.randint(0, 30 * 24 * 60))
        delta = random.randint(10, 240) if pri in ("P3", "P4") else random.randint(5, 180)
        resolved = created + timedelta(minutes=delta)

        title = random.choice(TEMPLATES[cat])
        desc = f"{title} - impactando usuários. Verificar logs e status."

        rows.append({
            "ticket_id": f"INC{i:06d}",
            "created_at": created.isoformat(timespec="seconds"),
            "resolved_at": resolved.isoformat(timespec="seconds"),
            "priority": pri,
            "category": cat,
            "title": title,
            "description": desc,
            "requester": f"user{random.randint(1,120):03d}@empresa.com",
        })

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"OK: {out_path} ({len(rows)} linhas)")

if __name__ == "__main__":
    main()
