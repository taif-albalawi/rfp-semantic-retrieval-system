from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

# =========================
# Embeddings
# =========================
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# =========================
# Load FAISS
# =========================
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# =========================
# LLM
# =========================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# =========================
# Refusal Logic
# =========================
def is_refusal(answer: str) -> bool:
    keywords = [
        "i don't know",
        "not enough information",
        "no information",
        "not mentioned",
        "cannot find"
    ]
    return any(k in answer.lower() for k in keywords)

# =========================
# MAIN RAG FUNCTION
# =========================
def get_answer(query: str):

    # Retrieval
    docs = vectorstore.similarity_search(query, k=5)

    context = "\n\n".join(
        [d.page_content for d in docs]
    )

    # Sources
    sources = list(set([
        os.path.basename(
            doc.metadata.get("source", "Unknown")
        )
        for doc in docs
    ]))

    # Prompt
    prompt = f"""
You are an RFP assistant.

Use ONLY the context below to answer.

If the answer is not in the context, say exactly:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{query}

Instructions:
- Answer ONLY using the provided context.
- Do not make up information.
- Format the answer as bullet points.
- Put EACH bullet point on a new line.
- Keep the answer concise and professional.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }