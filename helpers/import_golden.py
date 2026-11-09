"""One-off: convert ask-my-pdf's golden_set.jsonl into data/golden_v1.jsonl (bench TestCase format)."""
import json
import sys

from bench.datasets import TestCase

SRC = "/Users/angelmaldonado/Documents/projects/ask-my-pdf/eval/golden_set.jsonl"
DST = "data/golden_v1.jsonl"


def convert(row: dict) -> TestCase:
    return TestCase(
        id=row["id"],
        question=row["question"],
        doc=row["doc"],
        ground_truth=row["answer"],
        tags=[row["type"]],
        source=row["section"],
        source_pages=row["source_pages"],
    )


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    with open(src, encoding="utf-8") as f:
        test_cases = [convert(json.loads(line)) for line in f if line.strip()]
    with open(DST, "w", encoding="utf-8") as f:
        for c in test_cases:
            f.write(c.model_dump_json() + "\n")
    print(f"wrote {len(test_cases)} test_cases to {DST}")
