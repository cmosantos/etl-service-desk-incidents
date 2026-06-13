import unittest

from src.transform import classify_text, transform


class TestClassification(unittest.TestCase):
    def test_classifies_microsoft_365_incident(self):
        self.assertEqual(classify_text("Outlook não abre no Microsoft 365"), "M365")

    def test_classifies_network_incident(self):
        self.assertEqual(classify_text("VPN com latência alta"), "Rede")

    def test_classifies_access_incident(self):
        self.assertEqual(classify_text("Usuário bloqueado e MFA falhando"), "Acesso")

    def test_uses_server_as_default_category(self):
        self.assertEqual(classify_text("CPU alta na máquina virtual"), "Servidor")


class TestTransform(unittest.TestCase):
    def test_enriches_incident_and_flags_sla_breach(self):
        rows = [
            {
                "ticket_id": "INC000001",
                "created_at": "2025-01-01T10:00:00",
                "resolved_at": "2025-01-01T12:30:00",
                "priority": "P2",
                "category": "M365",
                "title": "Outlook não abre",
                "description": "Aplicativo apresenta erro ao iniciar",
                "requester": "user001@empresa.com",
            }
        ]

        clean_rows, metrics = transform(rows)

        self.assertEqual(metrics, {"rows_in": 1, "rows_out": 1, "dropped": 0})
        self.assertEqual(clean_rows[0]["resolution_minutes"], 150)
        self.assertEqual(clean_rows[0]["sla_minutes"], 120)
        self.assertEqual(clean_rows[0]["is_sla_breach"], 1)
        self.assertEqual(clean_rows[0]["category_pred"], "M365")

    def test_removes_duplicate_ticket_ids(self):
        base_row = {
            "ticket_id": "INC000002",
            "created_at": "2025-01-01T10:00:00",
            "resolved_at": "2025-01-01T10:30:00",
            "priority": "P3",
            "category": "Rede",
            "title": "VPN caiu",
            "description": "Falha de conexão",
            "requester": "user002@empresa.com",
        }

        clean_rows, _ = transform([base_row, dict(base_row)])

        self.assertEqual(len(clean_rows), 1)

    def test_drops_rows_without_ticket_id(self):
        rows = [
            {
                "ticket_id": "",
                "created_at": "2025-01-01T10:00:00",
                "resolved_at": "2025-01-01T10:30:00",
                "priority": "P3",
                "category": "Rede",
                "title": "VPN caiu",
                "description": "Falha de conexão",
                "requester": "user003@empresa.com",
            }
        ]

        clean_rows, metrics = transform(rows)

        self.assertEqual(clean_rows, [])
        self.assertEqual(metrics["dropped"], 1)


if __name__ == "__main__":
    unittest.main()
