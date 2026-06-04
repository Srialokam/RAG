from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def ingest_pdf(pdf_path: str):
    print(f"Loading PDF: {pdf_path}")
    
    # Step 1 - Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")

    # Step 2 - Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    # Step 3 - Embed and store
    print("Embedding and storing chunks...")
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print(f"Done. {len(chunks)} chunks stored in ChromaDB")
    return vectorstore

if __name__ == "__main__":
    pdf_path = "./data/Mastering_dbt_Core_Enhanced_Edition.pdf"
    ingest_pdf(pdf_path)