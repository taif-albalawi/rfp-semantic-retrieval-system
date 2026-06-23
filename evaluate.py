from rag_chain import get_answer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

EVAL_SET = [
    "What is this RFP about?",
    "What services are mentioned?",
    "What is the business problem?",
    "Who is the client?",
    "What technical requirements are mentioned?"
]

def evaluate():

    results = []

    for q in EVAL_SET:

        docs = vectorstore.similarity_search(q, k=5)
        answer = get_answer(q)

        results.append({
            "question": q,
            "answer": answer,
            "retrieved_docs": len(docs)
        })

        print("\nQ:", q)
        print("A:", answer[:200])
        print("-" * 40)

    return results


if __name__ == "__main__":
    output = evaluate()

    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Saved.")