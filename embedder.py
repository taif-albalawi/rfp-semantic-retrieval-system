import json
from sentence_transformers import SentenceTransformer

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Total chunks:", len(chunks))

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["content"] for chunk in chunks]

embeddings = model.encode(texts, show_progress_bar=True)

print("Embeddings shape:", embeddings.shape)
print("First vector sample:", embeddings[0][:5])