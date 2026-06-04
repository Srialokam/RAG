import streamlit as st
from src.chat import ask

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

# Chat history - persists during session
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

    # Get answer
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            result = ask(question)
        
        st.markdown(result["answer"])
        st.caption(f"📄 Sources: {', '.join(result['sources'])}")

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })