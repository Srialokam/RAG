from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

def ask(question: str, chat_history: list = []):
    # Step 1 - Retrieve relevant chunks
    vectorstore = load_vectorstore()
    chunks = vectorstore.similarity_search(question, k=4)

    # Step 2 - Build context from chunks
    context = "\n\n".join([chunk.page_content for chunk in chunks])
    sources = list(set([
        f"Page {chunk.metadata.get('page', 'N/A')}"
        for chunk in chunks
    ]))

    # Step 3 - Build prompt with memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that answers questions about dbt (data build tool).
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    # Step 4 - Build chat history messages
    history_messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            history_messages.append(AIMessage(content=msg["content"]))

    # Step 5 - Call LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question,
        "chat_history": history_messages
    })

    return {
        "answer": response.content,
        "sources": sources
    }

if __name__ == "__main__":
    # Test conversation memory
    history = []

    q1 = "What is the medallion architecture?"
    r1 = ask(q1, history)
    print(f"Q: {q1}")
    print(f"A: {r1['answer']}\n")
    history.append({"role": "user", "content": q1})
    history.append({"role": "assistant", "content": r1["answer"]})

    q2 = "Can you expand on the Silver layer?"
    r2 = ask(q2, history)
    print(f"Q: {q2}")
    print(f"A: {r2['answer']}\n")