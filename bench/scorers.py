"""Deterministic scorers first, judged scorers second."""




# def retrieval_recall(contexts: list[str], evidence: str) -> float: #did retrieval find the evidence
#     #golden set has evidence strings that must appear in the right chunk. check whether each evidence string appears in at least one retrieved context
#     """
#     - normalize before mathcing (lowecase everyint etc)
#     - unanswearble questions have empty evidence so maybe skip them?
#     - if recall is low, fix retreival not the prompt

#     """
#     raise NotImplementedError("TODO")


# def judge(question: str, answer: str, reference: str) -> dict:
#     """Use a judge model from a different family than the one being tested. Temperature 0. Return {'score', 'reason'}."""
#     raise NotImplementedError("TODO")


def precision_at_k(retrieved, relevant, k):
    if not relevant:
        return None
    
    top_k = retrieved[:k]
    hits = len(set(top_k) & set(relevant))
    return hits / k


def recall_at_k(retrieved, relevant, k):
    if not relevant:
        return None

    top_k = retrieved[:k]
    hits = len(set(top_k) & set(relevant))
    return hits / len(set(relevant))