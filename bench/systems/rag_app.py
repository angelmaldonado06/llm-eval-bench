import os, sys, time

RAG_APP_ROOT = "/Users/angelmaldonado/Documents/projects/ask-my-pdf"
sys.path.insert(0, os.path.join(RAG_APP_ROOT, "src"))
os.chdir(RAG_APP_ROOT)

# from retrieve import get_retriever
# from generate import build_chain

# _retriever = get_retriever() # returns EnsembleRetreiver
# _chain = build_chain(_retriever)

# def system(question: str) -> dict:
#     start_time = time.perf_counter()

#     docs = _retriever.invoke(question)
#     answer = _chain.invoke(question) #ai answer
    
#     end_time = time.perf_counter()

#     return {
#         "answer":answer,
#         "contexts": [d.page_content for d in docs],
#         "latency_sec": end_time - start_time
#     }


# if __name__ == "__main__":
#     out = system("What is overfitting?")
#     print(out["answer"])
#     print(len(out["contexts"]), out["latency_sec"])




from app import ask
from langchain_core.tracers.context import collect_runs

with collect_runs() as cb:
    answer = ask("test_data/intro_ml_textbook_ch4-6.pdf", "What is overfitting?")    # your app, untouched


docs=[]
for run in cb.traced_runs:                    # top-level runs, in call order
    if run.run_type == "retriever":
        docs = run.outputs["documents"]       # real Document objects, metadata included
        break

print(answer)
print(len(docs), "chunks")
for d in docs:
    print(d.metadata.get("page_label"), "|", d.page_content,"\n")


def show(run, depth=0):
    secs = (run.end_time - run.start_time).total_seconds()
    print("  " * depth + f"{run.run_type:10} {run.name}  {secs:.2f}s")
    for child in run.child_runs:
        show(child, depth + 1)
for r in cb.traced_runs:
    show(r)

# if __name__ == "__main__":
#     path = 
#     out = ask("What is overfitting?")
#     print(out["answer"])
#     print(len(out["contexts"]), out["latency_sec"])
