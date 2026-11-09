import json
import os

from bench.datasets import load_dataset
from bench.runner import run

# build absolute paths BEFORE importing rag_app, because the import changes the working directory
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET = os.path.join(REPO, "data", "golden_v1.jsonl")
CACHE = os.path.join(REPO, "runs", "cache")

from bench.systems.rag_app import system  # noqa: E402

test_cases = [
    t for t in load_dataset(DATASET)
    if t.doc == "intro_ml_textbook_ch4-6.pdf"
][:3]

result = run(system, test_cases, "hybrid-k3", "v2", "golden_v1", cache_dir=CACHE)

print(json.dumps(result["meta"], indent=2))
first = result["results"][0]
print(first["id"], first["doc"])
print(first["answer"])
print(len(first["contexts"]), first["latency_sec"])
