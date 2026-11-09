"""Immutable, versioned test sets."""
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    id: str = Field(..., description="The unique id for the question")
    question: str = Field(..., description="question to test")
    doc: str = Field(..., description="name of the PDF this question is asked about")
    ground_truth: str | None = Field(None, description="the correct answer")
    tags: list[str] = Field(..., description="category of question")
    source: str = Field("", description="where the answer can be found in the PDF (empty if unanswerable)")
    source_pages: list[int] = Field([], description="pages containing the answer")


def load_dataset(path: str) -> list[TestCase]:
    test_cases = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                test_cases.append(TestCase.model_validate_json(line))
            except ValueError as e:
                raise ValueError(f"Error parsing TestCase BaseModel: {e}")
            
    ids = [c.id for c in test_cases]
    dupes = {i for i in ids if ids.count(i) > 1}

    if dupes:
        raise ValueError(f"duplicate test_case ids")
    
    return test_cases



if __name__ == "__main__":
    print(load_dataset("data/golden_v1.jsonl"))