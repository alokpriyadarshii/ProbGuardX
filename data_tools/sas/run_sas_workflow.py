#!/usr/bin/env python3
"""Run the SAS customer feature workflow, with a local fallback.

If Base SAS is installed, this launcher executes customer_feature_engineering.sas.
If SAS is unavailable, it runs a standard-library fallback that mirrors the SAS
workflow outputs from the same CSV: PROC SQL-style summaries, PROC MEANS-style
statistics, PROC FREQ-style crosstabs, and a churn scoring baseline.
"""

from __future__ import annotations

import argparse
import csv
import math
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data_tools" / "sas" / "sas_customer_activity.csv"
DEFAULT_PROGRAM = ROOT / "data_tools" / "sas" / "customer_feature_engineering.sas"


def load_features(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"No customer activity rows found in {path}")

    features: list[dict[str, Any]] = []
    for row in rows:
        signup_dt = date.fromisoformat(row["signup_date"])
        event_dt = date.fromisoformat(row["event_date"])
        sessions = int(row["sessions"] or 0)
        support_tickets = int(row["support_tickets"] or 0)
        spend = float(row["spend"] or 0.0)
        spend_per_session = spend / sessions if sessions > 0 else None
        support_load = support_tickets / sessions if sessions > 0 else None
        if support_load is None:
            risk_segment = ""
        elif support_load >= 0.40:
            risk_segment = "high"
        elif support_load >= 0.10:
            risk_segment = "medium"
        else:
            risk_segment = "low"

        features.append(
            {
                "customer_id": row["customer_id"],
                "region": row["region"],
                "channel": row["channel"],
                "signup_dt": signup_dt,
                "event_dt": event_dt,
                "tenure_days": (event_dt - signup_dt).days,
                "spend": spend,
                "sessions": sessions,
                "support_tickets": support_tickets,
                "clicked_offer": int(row["clicked_offer"] or 0),
                "churned": int(row["churned"] or 0),
                "spend_per_session": spend_per_session,
                "support_load": support_load,
                "risk_segment": risk_segment,
            }
        )
    return features


def format_float(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "."
    return f"{value:.{digits}f}"


def print_sql_summary(rows: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["region"], row["channel"])].append(row)

    print("\nPROC SQL: work.region_channel_summary")
    print("region  channel  customers  total_spend  avg_sessions  churn_rate  offer_click_rate")
    for (region, channel), members in sorted(groups.items()):
        print(
            f"{region:<6}  {channel:<7}  {len({row['customer_id'] for row in members}):>9}  "
            f"{sum(row['spend'] for row in members):>11.2f}  "
            f"{mean(row['sessions'] for row in members):>12.2f}  "
            f"{mean(row['churned'] for row in members):>10.3f}  "
            f"{mean(row['clicked_offer'] for row in members):>16.3f}"
        )


def describe(values: list[float]) -> tuple[int, float, float, float | None, float, float]:
    count = len(values)
    std = stdev(values) if count > 1 else None
    return count, mean(values), median(values), std, min(values), max(values)


def print_means(rows: list[dict[str, Any]]) -> None:
    variables = ["spend", "sessions", "support_tickets", "tenure_days", "spend_per_session"]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["region"], row["channel"])].append(row)

    print("\nPROC MEANS: n mean median std min max")
    print("region  channel  variable             n      mean    median       std       min       max")
    for (region, channel), members in sorted(groups.items()):
        for variable in variables:
            values = [float(row[variable]) for row in members if row[variable] is not None]
            count, avg, med, std, low, high = describe(values)
            print(
                f"{region:<6}  {channel:<7}  {variable:<18}  {count:>2}  "
                f"{avg:>8.2f}  {med:>8.2f}  {format_float(std):>8}  {low:>8.2f}  {high:>8.2f}"
            )


def print_crosstab(rows: list[dict[str, Any]], left: str, right: str) -> None:
    left_values = sorted({row[left] for row in rows})
    right_values = sorted({row[right] for row in rows})
    counts = Counter((row[left], row[right]) for row in rows)

    print(f"\nPROC FREQ: {left}*{right}")
    print(f"{left:<14}  " + "  ".join(f"{str(value):>8}" for value in right_values) + "     total")
    for left_value in left_values:
        row_total = sum(counts[(left_value, right_value)] for right_value in right_values)
        values = "  ".join(f"{counts[(left_value, right_value)]:>8}" for right_value in right_values)
        print(f"{str(left_value):<14}  {values}  {row_total:>8}")


def sigmoid(value: float) -> float:
    value = max(-35.0, min(35.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def print_logistic_scores(rows: list[dict[str, Any]]) -> None:
    columns = ["support_tickets", "clicked_offer", "spend_per_session", "tenure_days"]
    means = {column: mean(float(row[column]) for row in rows) for column in columns}
    scales = {
        column: math.sqrt(mean((float(row[column]) - means[column]) ** 2 for row in rows)) or 1.0
        for column in columns
    }
    matrix = [
        [1.0] + [(float(row[column]) - means[column]) / scales[column] for column in columns]
        for row in rows
    ]
    labels = [row["churned"] for row in rows]
    weights = [0.0 for _ in matrix[0]]
    learning_rate = 0.08

    for _ in range(1200):
        gradients = [0.0 for _ in weights]
        for features, label in zip(matrix, labels):
            prediction = sigmoid(sum(weight * value for weight, value in zip(weights, features)))
            for index, value in enumerate(features):
                gradients[index] += (prediction - label) * value
        for index in range(len(weights)):
            weights[index] -= learning_rate * gradients[index] / len(rows)

    scored = []
    for row, features in zip(rows, matrix):
        scored.append(
            {
                "customer_id": row["customer_id"],
                "region": row["region"],
                "channel": row["channel"],
                "churned": row["churned"],
                "predicted_churn_probability": sigmoid(
                    sum(weight * value for weight, value in zip(weights, features))
                ),
            }
        )

    print("\nPROC LOGISTIC: work.churn_scores")
    print("customer_id  region  channel  churned  predicted_churn_probability")
    for row in sorted(scored, key=lambda item: item["predicted_churn_probability"], reverse=True)[:8]:
        print(
            f"{row['customer_id']:<11}  {row['region']:<6}  {row['channel']:<7}  "
            f"{row['churned']:>7}  {row['predicted_churn_probability']:>29.3f}"
        )


def run_fallback(data_path: Path, program_path: Path) -> int:
    print("SAS runtime not found; running local SAS-equivalent fallback.")
    print(f"SAS source: {program_path}")
    print(f"Input data:  {data_path}")
    rows = load_features(data_path)
    print_sql_summary(rows)
    print_means(rows)
    print_crosstab(rows, "region", "churned")
    print_crosstab(rows, "channel", "clicked_offer")
    print_crosstab(rows, "risk_segment", "churned")
    print_logistic_scores(rows)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SAS workflow or local fallback")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--program", type=Path, default=DEFAULT_PROGRAM)
    parser.add_argument("--force-fallback", action="store_true")
    args = parser.parse_args()

    sas_binary = shutil.which("sas")
    if sas_binary and not args.force_fallback:
        print(f"Found SAS runtime: {sas_binary}")
        completed = subprocess.run([sas_binary, str(args.program)], cwd=ROOT)
        return completed.returncode

    return run_fallback(args.data, args.program)


if __name__ == "__main__":
    raise SystemExit(main())
