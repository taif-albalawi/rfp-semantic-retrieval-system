from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# =========================
# Metadata Filtering (MVP)
# =========================
def retrieve(query: str, k: int = 4, source_filter: str = None):

    if source_filter:
        docs = vectorstore.similarity_search(
            query,
            k=k,
            filter={"source": source_filter}
        )
    else:
        docs = vectorstore.similarity_search(query, k=k)

    return docs