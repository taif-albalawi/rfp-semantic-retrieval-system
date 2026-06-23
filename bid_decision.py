from rag_chain import vectorstore
from llm import get_llm

llm = get_llm()

def bid_no_bid(query: str):

    docs = vectorstore.similarity_search(query, k=5)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are an RFP Bid/No-Bid assistant.

Decide if the company should:
- BID
- NO-BID
- MAYBE

Use ONLY the context.

Context:
{context}

RFP Summary:
{query}

Rules:
- If project matches expertise → BID
- If missing info or risky → NO-BID
- If unclear → MAYBE

Return:
- Decision
- Reason (bullet points)
"""

    response = llm.invoke(prompt)
    return response.content