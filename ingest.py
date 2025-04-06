import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

def create_index():
    os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY_HERE"
    
    URLs = [
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=GDF5PQP4Z6SUH4CQ",
        "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GW2QNFK3F7T8ULDS"
    ]
    
    print("Loading documents...")
    loader = WebBaseLoader(web_paths=URLs)
    docs = loader.load()
    
    for data_content in docs:
        data_content.page_content = data_content.page_content.replace("\n", " ")
    
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )
    chunks = text_splitter.split_documents(docs)
    
    print("Initializing embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print("Creating vector database...")
    try:
        client = QdrantClient(path="./buildwithai-udaipur")
        client.create_collection(
            collection_name="rag",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    except RuntimeError:
        # Collection might already exist
        client = QdrantClient(path="./buildwithai-udaipur")
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag",
        embedding=embeddings,
    )
    vector_store.add_documents(chunks)
    
    print("Index created successfully!")
    return True

if __name__ == "__main__":
    create_index()