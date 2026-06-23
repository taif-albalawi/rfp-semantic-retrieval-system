import json
import chromadb
from sentence_transformers import SentenceTransformer

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Total chunks:", len(chunks))

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="rfp_chunks")

texts = [chunk["content"] for chunk in chunks]

metadatas = [
    {
        "doc_id": chunk["doc_id"],
        "source": chunk["source"],
        "file_type": chunk.get("file_type", ""),
        "folder": chunk.get("folder", ""),
        "chunk_id": chunk["chunk_id"]
    }
    for chunk in chunks
]

ids = [
    f'{chunk["doc_id"]}_{chunk["chunk_id"]}'
    for chunk in chunks
]

embeddings = model.encode(texts, show_progress_bar=True).tolist()

batch_size = 5000

for i in range(0, len(texts), batch_size):
    collection.add(
        documents=texts[i:i + batch_size],
        embeddings=embeddings[i:i + batch_size],
        metadatas=metadatas[i:i + batch_size],
        ids=ids[i:i + batch_size]
    )

    print(f"Added batch {i // batch_size + 1}")

print("Saved to Chroma DB successfully")
print("Collection count:", collection.count())