import pandas as pd
from src.transform import transform

def test_transform_outputs_columns():
    df = pd.DataFrame([{
        "ticket_id":"INC000001",
        "created_at":"2025-12-01T10:00:00",
        "resolved_at":"2025-12-01T11:00:00",
        "priority":"P2",
        "category":"Rede",
        "title":"VPN caiu",
        "description":"Usuários sem acesso",
    }])
    out, metrics = transform(df)
    assert "resolution_minutes" in out.columns
    assert "is_sla_breach" in out.columns
    assert "category_pred" in out.columns
    assert isinstance(metrics, dict)
