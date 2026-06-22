"""Reduce step for customer activity aggregation.

Input: sorted tab-separated key/value pairs from mapper.py.
Output: region-level aggregates.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable, Iterator


def reduce_pairs(lines: Iterable[str]) -> Iterator[str]:
    current_region = None
    customers = 0
    total_spend = 0.0
    total_sessions = 0
    churns = 0

    def flush() -> str:
        churn_rate = churns / customers if customers else 0.0
        avg_sessions = total_sessions / customers if customers else 0.0
        return f"{current_region}\t{customers}\t{total_spend:.2f}\t{avg_sessions:.2f}\t{churn_rate:.3f}"

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        region, payload = line.split("\t", 1)
        count_s, spend_s, sessions_s, churn_s = payload.split(",")

        if current_region is not None and region != current_region:
            yield flush()
            customers = 0
            total_spend = 0.0
            total_sessions = 0
            churns = 0

        current_region = region
        customers += int(count_s)
        total_spend += float(spend_s)
        total_sessions += int(sessions_s)
        churns += int(churn_s)

    if current_region is not None:
        yield flush()


def main() -> None:
    print("region\tcustomers\ttotal_spend\tavg_sessions\tchurn_rate")
    for output_line in reduce_pairs(sys.stdin):
        print(output_line)


if __name__ == "__main__":
    main()
