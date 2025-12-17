import unittest
from src.transform import transform

class TestTransform(unittest.TestCase):
    def test_transform_adds_fields(self):
        rows = [{
            "ticket_id": "INC000001",
            "created_at": "2025-12-01T10:00:00",
            "resolved_at": "2025-12-01T11:00:00",
            "priority": "P2",
            "category": "Rede",
            "title": "VPN caiu",
            "description": "Usuários sem acesso",
            "requester": "user001@empresa.com",
        }]
        out, metrics = transform(rows)
        self.assertEqual(metrics["rows_out"], 1)
        self.assertIn("resolution_minutes", out[0])
        self.assertIn("is_sla_breach", out[0])
        self.assertIn("category_pred", out[0])

if __name__ == "__main__":
    unittest.main()
