import random
from datetime import datetime, timedelta
import pandas as pd

CATEGORIES = ["Rede", "Servidor", "M365", "Acesso", "Backup"]
PRIORITIES = ["P1", "P2", "P3", "P4"]

TEMPLATES = {
    "Rede": ["Link intermitente", "Perda de pacote", "VPN caiu", "Switch sem resposta", "Latência alta"],
    "Servidor": ["CPU alta", "Disco cheio", "Serviço não inicia", "Reboot inesperado", "VM travada"],
    "M365": ["Outlook não abre", "Login falhando", "Teams com erro", "Exchange com atraso", "Defender alerta"],
    "Acesso": ["Usuário bloqueado", "Senha expirada", "Sem permissão", "MFA falhando", "Conta desabilitada"],
    "Backup": ["Job falhou", "Backup lento", "Restore necessário", "Veeam erro", "Storage sem espaço"],
}

def main(out_path="data/raw/incidents.csv", n=500, seed=42):
    random.seed(seed)
    base = datetime.now() - timedelta(days=30)

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
            "created_at": created.isoformat(),
            "resolved_at": resolved.isoformat(),
            "priority": pri,
            "category": cat,
            "title": title,
            "description": desc,
            "requester": f"user{random.randint(1,120):03d}@empresa.com",
        })

    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)
    print(f"OK: {out_path} ({len(df)} linhas)")

if __name__ == "__main__":
    main()
