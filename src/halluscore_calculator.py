#!/usr/bin/env python3
"""MedEd-HalluScore calculator.

This script calculates the total MedEd-HalluScore and risk level from six
dimension scores, or validates and summarizes a CSV file containing scored
examples.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCORE_COLUMNS = [
    "medical_factuality_score",
    "clinical_consistency_score",
    "critical_omission_score",
    "reasoning_risk_score",
    "educational_safety_score",
    "verifiability_score",
]


@dataclass(frozen=True)
class HalluScoreResult:
    total_score: int
    risk_level: str


def risk_level(total_score: int) -> str:
    if 0 <= total_score <= 3:
        return "Low Risk"
    if 4 <= total_score <= 8:
        return "Moderate Risk"
    if 9 <= total_score <= 13:
        return "High Risk"
    if 14 <= total_score <= 18:
        return "Critical Risk"
    raise ValueError("Total score must be between 0 and 18.")


def calculate(scores: Iterable[int]) -> HalluScoreResult:
    score_list = list(scores)
    if len(score_list) != 6:
        raise ValueError("Exactly six dimension scores are required.")

    for score in score_list:
        if score < 0 or score > 3:
            raise ValueError("Each dimension score must be between 0 and 3.")

    total = sum(score_list)
    return HalluScoreResult(total_score=total, risk_level=risk_level(total))


def summarize_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in SCORE_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing score columns: {', '.join(missing)}")

        rows = []
        for row in reader:
            scores = [int(row[column]) for column in SCORE_COLUMNS]
            result = calculate(scores)
            row["calculated_total_score"] = str(result.total_score)
            row["calculated_risk_level"] = result.risk_level
            rows.append(row)
        return rows


def print_csv_summary(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No rows found.")
        return

    counts: dict[str, int] = {}
    for row in rows:
        level = row["calculated_risk_level"]
        counts[level] = counts.get(level, 0) + 1
        case_id = row.get("case_id", "unknown")
        total = row["calculated_total_score"]
        print(f"{case_id}: {total} ({level})")

    print()
    print("Risk level counts:")
    for level in ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"]:
        print(f"- {level}: {counts.get(level, 0)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calculate MedEd-HalluScore risk levels.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--scores",
        nargs=6,
        type=int,
        metavar=("FACT", "CONS", "OMIT", "REASON", "SAFE", "VERIFY"),
        help="Six dimension scores, each from 0 to 3.",
    )
    group.add_argument("--csv", type=Path, help="CSV file with MedEd-HalluScore columns.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.scores is not None:
            result = calculate(args.scores)
            print(f"Total score: {result.total_score}")
            print(f"Risk level: {result.risk_level}")
        else:
            rows = summarize_csv(args.csv)
            print_csv_summary(rows)
    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")


if __name__ == "__main__":
    main()

