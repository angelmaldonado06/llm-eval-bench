# LLM eval bench

A small harness that turns 'this prompt feels better' into a number you can defend. Run your RAG app over a versioned test set, score it with deterministic checks plus an LLM judge, compare runs, and fail a pull request when quality drops. Portfolio path, step 2 of 5: point it at your RAG app right away.

**RAG type:** Advanced RAG  ·  **Difficulty:** Advanced  ·  **Time:** 2 weekends

## Goals
- [ ] Versioned datasets (inputs, reference answers, tags, difficulty)
- [ ] Task runner with caching so re-scoring is free
- [ ] Scorers: exact match, retrieval recall, and an LLM judge with a written rubric
- [ ] Judge calibration: label 100 examples by hand and report agreement (Cohen's kappa)
- [ ] Run-to-run comparison with confidence intervals
- [ ] A GitHub Action that fails when a score drops below a threshold

## Stretch goals
- [ ] Pairwise comparison with Elo ratings
- [ ] Cost-versus-quality plot to pick the cheapest model that clears the bar
- [ ] Mine hard cases from failed runs into the dataset

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then add your keys
```

## Run
```bash
python -m bench.run --dataset data/golden_v1.jsonl --system rag_app
python -m bench.compare runs/run_a.json runs/run_b.json
```

## Results
Fill this in as you improve the system. Numbers here are what make the project stand out.

| Version | Judge-human agreement (kappa) | Regression detection rate | Cost per run ($) | Suite time (s) |
|---|---|---|---|---|
| baseline |   |   |   |   |

## Design decisions
- Why this loader / splitter / embedding model / store:
- What I tried that did not work:




llm-eval-bench/
├── bench/                      # generic: never mentions a specific app
│   ├── __init__.py
│   ├── system.py           ★   RAGSystem (abstract), SystemOutput, Chunk
│   ├── datasets.py             TestCase + load_dataset (yours, made generic)
│   ├── runner.py               Runner class (your run() logic moves in)
│   ├── scorers.py              recall_at_k, precision_at_k, contains_fact (functions)
│   ├── judge.py            ★   Judge class (the one scorer with state)
│   ├── calibrate.py            Cohen's kappa
│   ├── compare.py              run A vs run B + bootstrap CI
│   └── run.py              ★   command line: --system ask_my_pdf --dataset ...
│
├── adapters/                   # one file per app, the only app-specific code
│   ├── __init__.py
│   └── ask_my_pdf.py       →   from bench/systems/rag_app.py (your collect_runs script)
│
├── datasets/
│   └── ask_my_pdf/
│       ├── v1.jsonl        →   from data/golden_v1.jsonl (never edit it again)
│       └── v2.jsonl        ★   generic fields: reference, relevant_sources, metadata
│
├── helpers/                    # one-off scripts
│   ├── import_golden.py
│   └── v1_to_v2.py         ★   converts v1 into v2
│
├── runs/                       # outputs, add to .gitignore
│   ├── cache/                  cached answers (you already have this)
│   └── ask-my-pdf-hybrid-k3.json   one report per run
│
├── .github/workflows/eval.yml  CI gate (last step)
├── requirements.txt
└── README.md
