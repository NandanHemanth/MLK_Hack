import os
import requests
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API keys and endpoints from .env
GEMINI_EMBED_API_KEY = os.getenv("GEMINI_EMBED_API_KEY")
GEMINI_EMBED_ENDPOINT = os.getenv("GEMINI_EMBED_ENDPOINT")
GEMINI_LLM_API_KEY = os.getenv("GEMINI_LLM_API_KEY")
GEMINI_LLM_ENDPOINT = os.getenv("GEMINI_LLM_ENDPOINT")

# === Embedding Function ===
def gemini_embed(texts, api_key, endpoint):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"texts": texts}
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    return response.json().get("embeddings", [])

# === LLM Function ===
def gemini_generate(prompt, api_key, endpoint):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"prompt": prompt}
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    return response.json().get("generated_text", "")

# === File Processing ===
def load_file(file_path):
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide a .txt or .pdf file.")
    
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# === RAG System ===
def build_rag_system(file_path, embed_api_key, embed_endpoint, llm_api_key, llm_endpoint):
    documents = load_file(file_path)
    document_texts = [doc.page_content for doc in documents]
    embeddings = gemini_embed(document_texts, api_key=embed_api_key, endpoint=embed_endpoint)
    retriever = FAISS.from_texts(document_texts, embeddings).as_retriever()

    def query_rag_system(query):
        relevant_docs = retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        full_prompt
