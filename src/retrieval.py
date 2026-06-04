from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

def retrieve_chunks(question: str, k: int = 4):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(question, k=k)
    return results

if __name__ == "__main__":
    question = "What is the difference between dbt Core and dbt Cloud?"
    chunks = retrieve_chunks(question)
    
    print(f"\nQuestion: {question}")
    print(f"\nTop {len(chunks)} relevant chunks:\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} (page {chunk.metadata.get('page', 'N/A')}) ---")
        print(chunk.page_content)
        print()