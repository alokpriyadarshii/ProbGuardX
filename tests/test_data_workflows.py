import csv
import tempfile
import unittest
from pathlib import Path

from data_tools.python.customer_feature_engineering import load_and_clean, supervised_baseline
from data_tools.sas.run_sas_workflow import load_features


FIELDNAMES = [
    "customer_id",
    "region",
    "channel",
    "signup_date",
    "event_date",
    "spend",
    "sessions",
    "support_tickets",
    "clicked_offer",
    "churned",
]


def write_csv(rows):
    handle = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
    path = Path(handle.name)
    try:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        handle.close()
    return path


class DataWorkflowInputTests(unittest.TestCase):
    def test_python_loader_rejects_empty_input(self):
        path = write_csv([])

        try:
            with self.assertRaisesRegex(ValueError, "No customer activity rows"):
                load_and_clean(path)
        finally:
            path.unlink()

    def test_python_loader_rejects_rows_without_spend_values(self):
        path = write_csv(
            [
                {
                    "customer_id": "P001",
                    "region": "North",
                    "channel": "web",
                    "signup_date": "2025-01-01",
                    "event_date": "2026-01-01",
                    "spend": "",
                    "sessions": "3",
                    "support_tickets": "1",
                    "clicked_offer": "0",
                    "churned": "0",
                }
            ]
        )

        try:
            with self.assertRaisesRegex(ValueError, "No usable spend values"):
                load_and_clean(path)
        finally:
            path.unlink()

    def test_supervised_baseline_rejects_empty_rows(self):
        with self.assertRaisesRegex(ValueError, "at least one row"):
            supervised_baseline([])

    def test_sas_loader_rejects_empty_input(self):
        path = write_csv([])

        try:
            with self.assertRaisesRegex(ValueError, "No customer activity rows"):
                load_features(path)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
