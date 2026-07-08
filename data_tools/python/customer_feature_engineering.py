"""Python data manipulation and model-ready feature engineering example.

This script demonstrates CSV ingestion, cleaning, date handling, aggregation,
feature creation, and a small supervised-learning baseline without requiring
third-party packages.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median
from typing import Any


DEFAULT_DATA = Path(__file__).resolve().with_name("python_customer_activity.csv")


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def load_and_clean(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"No customer activity rows found in {path}")

    spends = [float(row["spend"]) for row in rows if row["spend"]]
    if not spends:
        raise ValueError(f"No usable spend values found in {path}")

    median_spend = median(spends)

    cleaned: list[dict[str, Any]] = []
    for row in rows:
        cleaned.append(
            {
                "customer_id": row["customer_id"],
                "region": row["region"],
                "channel": row["channel"],
                "signup_date": parse_date(row["signup_date"]),
                "event_date": parse_date(row["event_date"]),
                "spend": float(row["spend"]) if row["spend"] else median_spend,
                "sessions": int(row["sessions"] or 0),
                "support_tickets": int(row["support_tickets"] or 0),
                "clicked_offer": int(row["clicked_offer"] or 0),
                "churned": int(row["churned"] or 0),
            }
        )
    return cleaned


def percentile(values: list[float], rank: float) -> float:
    if not values:
        raise ValueError("percentile requires at least one value")

    ordered = sorted(values)
    position = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * rank)))
    return ordered[position]


def engineer_features(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    high_value_cutoff = percentile([row["spend"] for row in rows], 0.75)
    features: list[dict[str, Any]] = []
    for row in rows:
        sessions = max(int(row["sessions"]), 1)
        support_load = row["support_tickets"] / sessions
        enriched = dict(row)
        enriched["tenure_days"] = (row["event_date"] - row["signup_date"]).days
        enriched["spend_per_session"] = row["spend"] / sessions
        enriched["support_load"] = support_load
        enriched["high_value"] = int(row["spend"] >= high_value_cutoff)
        if support_load >= 0.40:
            enriched["risk_segment"] = "high"
        elif support_load >= 0.10:
            enriched["risk_segment"] = "medium"
        else:
            enriched["risk_segment"] = "low"
        features.append(enriched)
    return features


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["region"], row["channel"])].append(row)

    summary = []
    for (region, channel), members in sorted(groups.items()):
        summary.append(
            {
                "region": region,
                "channel": channel,
                "customers": len({row["customer_id"] for row in members}),
                "total_spend": sum(row["spend"] for row in members),
                "avg_sessions": mean(row["sessions"] for row in members),
                "churn_rate": mean(row["churned"] for row in members),
                "offer_click_rate": mean(row["clicked_offer"] for row in members),
            }
        )
    return summary


def sigmoid(value: float) -> float:
    value = max(-35.0, min(35.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def supervised_baseline(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        raise ValueError("supervised_baseline requires at least one row")

    columns = ["spend", "sessions", "support_tickets", "clicked_offer", "tenure_days"]
    means = {column: mean(row[column] for row in rows) for column in columns}
    scales = {
        column: math.sqrt(mean((row[column] - means[column]) ** 2 for row in rows)) or 1.0
        for column in columns
    }

    matrix = [
        [1.0] + [(row[column] - means[column]) / scales[column] for column in columns]
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
        enriched = {
            "customer_id": row["customer_id"],
            "region": row["region"],
            "channel": row["channel"],
            "churned": row["churned"],
            "predicted_churn_probability": sigmoid(
                sum(weight * value for weight, value in zip(weights, features))
            ),
        }
        scored.append(enriched)
    return sorted(scored, key=lambda row: row["predicted_churn_probability"], reverse=True)


def print_summary(rows: list[dict[str, Any]]) -> None:
    print("region  channel  customers  total_spend  avg_sessions  churn_rate  offer_click_rate")
    for row in rows:
        print(
            f"{row['region']:<6}  {row['channel']:<7}  {row['customers']:>9}  "
            f"{row['total_spend']:>11.2f}  {row['avg_sessions']:>12.2f}  "
            f"{row['churn_rate']:>10.3f}  {row['offer_click_rate']:>16.3f}"
        )


def print_scores(rows: list[dict[str, Any]]) -> None:
    print("customer_id  region  channel  churned  predicted_churn_probability")
    for row in rows[:8]:
        print(
            f"{row['customer_id']:<11}  {row['region']:<6}  {row['channel']:<7}  "
            f"{row['churned']:>7}  {row['predicted_churn_probability']:>29.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Python data manipulation and ML baseline")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()

    features = engineer_features(load_and_clean(args.data))
    print("Aggregated customer features by region/channel")
    print_summary(summarize(features))
    print("\nTop churn-risk customers")
    print_scores(supervised_baseline(features))


if __name__ == "__main__":
    main()
