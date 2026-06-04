from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

def ask(question: str):
    # Step 1 - Retrieve relevant chunks
    vectorstore = load_vectorstore()
    chunks = vectorstore.similarity_search(question, k=4)
    
    # Step 2 - Build context from chunks
    context = "\n\n".join([chunk.page_content for chunk in chunks])
    sources = list(set([
        f"Page {chunk.metadata.get('page', 'N/A')}" 
        for chunk in chunks
    ]))

    # Step 3 - Build prompt
    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that answers questions about dbt (data build tool).
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question:
{question}

Answer:
""")

    # Step 4 - Call LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })

    return {
        "answer": response.content,
        "sources": sources
    }

if __name__ == "__main__":
    questions = [
        "What is the difference between dbt Core and dbt Cloud?",
        "How do snapshots work in dbt?",
        "What is the medallion architecture?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print("-" * 60)