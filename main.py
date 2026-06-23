from fastapi import FastAPI
from pydantic import BaseModel
from rag_chain import get_answer
from bid_decision import bid_no_bid

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: QueryRequest):

    result = get_answer(request.query)

    return {
        "query": request.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.post("/bid")
def bid(request: QueryRequest):
    return {
        "query": request.query,
        "decision": bid_no_bid(request.query)
    }