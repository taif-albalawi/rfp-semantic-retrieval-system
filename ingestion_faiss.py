from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path
import pandas as pd
import os

# =========================
# Embeddings
# =========================
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# =========================
# Load data
# =========================
folder_path = Path("data")

all_documents = []

for file_path in folder_path.rglob("*"):

    if not file_path.is_file():
        continue

    if file_path.suffix.lower() not in [".pdf", ".docx", ".xlsx", ".pptx"]:
        continue

    try:
        if file_path.suffix == ".pdf":
            all_documents.extend(PyPDFLoader(str(file_path)).load())

        elif file_path.suffix == ".docx":
            all_documents.extend(Docx2txtLoader(str(file_path)).load())

        elif file_path.suffix == ".xlsx":
            try:
                all_documents.extend(UnstructuredExcelLoader(str(file_path)).load())
            except:
                df = pd.read_excel(file_path)
                text = df.fillna("").astype(str).to_string()

                all_documents.append(
                    Document(page_content=text, metadata={"source": str(file_path)})
                )

        elif file_path.suffix == ".pptx":
              all_documents.extend(
        UnstructuredPowerPointLoader(str(file_path)).load()
    )

    except Exception as e:
        print("Skipped:", file_path.name, e)

print("Docs loaded:", len(all_documents))

# =========================
# Split
# =========================
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(all_documents)

print("Chunks:", len(chunks))

# =========================
# Build FAISS
# =========================
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_index")

print("FAISS index saved successfully")