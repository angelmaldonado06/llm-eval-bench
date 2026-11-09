"""Run a system over a dataset, cache outputs by (system version, prompt version, input)."""
import hashlib
import json
import os
from datetime import datetime


def cache_key(system_version: str, prompt_version: str, question: str) -> str:
    # any change to one of the three parts gives a new key, so old answers are never reused
    raw = "\x1f".join([system_version, prompt_version, question]) #special separator char
    return hashlib.sha256(raw.encode("utf-8")).hexdigest() #file name used to store the response


def run(system, test_cases, system_version, prompt_version, dataset, cache_dir="runs/cache"):
    # absolute, so a later os.chdir (rag_app does one) can't move the cache
    cache_dir = os.path.abspath(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)

    outputs = []
    for i, test_case in enumerate(test_cases, 1):
        path = os.path.join(cache_dir, cache_key(system_version, prompt_version, test_case.question) + ".json")

        if os.path.exists(path): #checking if the question was already answered
            with open(path, encoding="utf-8") as f:
                output = json.load(f)
        else:
            try:
                output = system(test_case.question) # call rag system to answer the question. returns dict with answer, context, and latency
            except Exception as e:
                # one failed question shouldn't lose the whole run; errors are not cached so a rerun retries them
                output = {"error": f"{e}"}
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(output, f, sort_keys=True)

        #adding information to the output
        output["id"] = test_case.id 
        output["doc"] = test_case.doc

        outputs.append(output) #append response to the list of all responses
        print(f"{i}/{len(test_cases)} {test_case.id}" + (" ERROR" if "error" in output else "")) #prints progress to terminal

    return {
        "meta": {
            "system_version": system_version,
            "prompt_version": prompt_version,
            "dataset": dataset,
            "docs": sorted({c.doc for c in test_cases}),
            "n_cases": len(test_cases),
            "n_errors": sum("error" in o for o in outputs),
            "timestamp": datetime.now().isoformat(timespec="seconds")
        },
        "results": outputs
    }
