import json

def rerank_by_overlap(question: str, contexts: list) -> list:
    q_words = set(question.lower().split())
    return sorted(
        contexts,
        key=lambda c: len(q_words.intersection(set(c.get("text", "").lower().split()))),
        reverse=True,
    )

with open("artifacts/actual_answers.json", "r") as f:
    raw_data = json.load(f)

if isinstance(raw_data, dict):
    if "answers" in raw_data:
        records = raw_data["answers"]
    elif "results" in raw_data:
        records = raw_data["results"]
    else:
        records = []
        for k, v in raw_data.items():
            if isinstance(v, dict):
                v.setdefault("id", k)
                records.append(v)
else:
    records = raw_data

target_ids = {"E02", "E05", "M02", "H01", "H05"}

for item in records:
    item_id = item.get("id")
    if item_id in target_ids:
        question = item.get("question", "")
        original_contexts = item.get("retrieved_contexts", [])
        reranked_contexts = rerank_by_overlap(question, original_contexts)

        print(f"\n--- Case {item_id} ---")
        print("Question:", question[:60] + "...")
        print("Original order :", [c.get("chunk_id", c.get("source_doc")) for c in original_contexts])
        print("Reranked order :", [c.get("chunk_id", c.get("source_doc")) for c in reranked_contexts])