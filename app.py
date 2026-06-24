import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="dbt Knowledge Assistant",
    page_icon="🔧",
    layout="centered"
)

# Header
st.title("🔧 dbt Knowledge Assistant")
st.caption("Ask anything about dbt Core — powered by RAG")
st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            st.caption(f"📄 Sources: {', '.join(message['sources'])}")

# Chat input
if question := st.chat_input("Ask a question about dbt..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Call FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question}
                )
                result = response.json()
                answer = result["answer"]
                sources = result["sources"]
            except Exception as e:
                answer = f"Error connecting to API: {str(e)}"
                sources = []

        st.markdown(answer)
        if sources:
            st.caption(f"📄 Sources: {', '.join(sources)}")

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })