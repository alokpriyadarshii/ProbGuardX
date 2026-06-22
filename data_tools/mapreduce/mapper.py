"""Map step for customer activity aggregation.

Input: CSV rows from stdin.
Output: tab-separated key/value pairs keyed by region.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Iterable, Iterator


def emit_pairs(rows: Iterable[dict[str, str]]) -> Iterator[str]:
    for row in rows:
        region = row["region"]
        spend = float(row["spend"] or 0.0)
        sessions = int(row["sessions"] or 0)
        churned = int(row["churned"] or 0)
        yield f"{region}\t1,{spend:.2f},{sessions},{churned}"


def main() -> None:
    reader = csv.DictReader(sys.stdin)
    for pair in emit_pairs(reader):
        print(pair)


if __name__ == "__main__":
    main()
