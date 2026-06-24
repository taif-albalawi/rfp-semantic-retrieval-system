import streamlit as st
import requests

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="RFP Semantic Retrieval System",
    page_icon="🤖",
    layout="centered"
)

# =========================
# Title
# =========================
st.title("🤖 RFP Intelligence System")
st.write("Ask questions or evaluate RFP decisions")

# =========================
# Mode Selection
# =========================
mode = st.selectbox(
    "Choose Mode",
    ["Q&A", "Bid / No-Bid"]
)

# =========================
# Input
# =========================
query = st.text_input("Enter your question:")

# =========================
# Run Button
# =========================
if st.button("Run") and query:

    try:
        # Select endpoint
        url = (
            "http://127.0.0.1:8000/ask"
            if mode == "Q&A"
            else "http://127.0.0.1:8000/bid"
        )

        response = requests.post(
            url,
            json={"query": query},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("📌 Result")

            # =========================
            # Q&A MODE
            # =========================
            if mode == "Q&A":

                answer = data.get("answer", "")

                # لو جا dict نحوله نص
                if isinstance(answer, dict):
                    answer = str(answer)

                st.subheader("📌 Answer")

                # ===== FIX: split lines correctly =====
                answer_lines = answer.split("\n")

                for line in answer_lines:
                    line = line.strip()
                    if line:
                        st.markdown(f"- {line}")

                # =========================
                # Sources
                # =========================
                st.subheader("📚 Sources")

                sources = data.get("sources", [])

                if isinstance(sources, str):
                    sources = [sources]

                if sources:
                    for i, s in enumerate(sources, 1):
                        st.write(f"{i}. {s}")
                else:
                    st.info("No sources found")

            # =========================
            # BID / NO-BID MODE
            # =========================
            else:

                decision = data.get("decision", "No decision found")
                reason = data.get("reason", "")

                st.subheader("⚖️ Decision")
                st.success(decision)

                if reason:
                    st.write(reason)

                sources = data.get("sources", [])

                if sources:
                    st.subheader("📚 Sources")
                    for i, s in enumerate(sources, 1):
                        st.write(f"{i}. {s}")

        else:
            st.error(f"Error calling API: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ FastAPI server is not running. Run uvicorn first.")

    except requests.exceptions.ReadTimeout:
        st.error("⏳ Request timeout. Try again.")