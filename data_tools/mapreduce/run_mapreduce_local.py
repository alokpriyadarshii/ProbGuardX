"""Local runner for the mapper/reducer pair without Hadoop.

This simulates the MapReduce contract: map records, sort by key, then reduce.
"""

from __future__ import annotations

import csv
from pathlib import Path

from mapper import emit_pairs
from reducer import reduce_pairs


DATA = Path(__file__).resolve().parents[1] / "customer_activity.csv"


def main() -> None:
    with DATA.open(newline="") as handle:
        mapped = sorted(emit_pairs(csv.DictReader(handle)))

    print("region\tcustomers\ttotal_spend\tavg_sessions\tchurn_rate")
    for line in reduce_pairs(mapped):
        print(line)


if __name__ == "__main__":
    main()
