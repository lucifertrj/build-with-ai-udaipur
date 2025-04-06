import streamlit as st
import os
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

st.set_page_config(page_title="Build with AI - RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Build with AI - RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

api_key = st.secrets["google_api_key"]
os.environ['GOOGLE_API_KEY'] = api_key

@st.cache_resource
def initialize_rag_pipeline():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")        
        client = QdrantClient(path="./buildwithai-udaipur")
        vector_store = QdrantVectorStore(
            client=client,
            collection_name="rag",
            embedding=embeddings,
        )
        
        retriever = vector_store.as_retriever()
        
        template = """You are an customer service assistant for question-answering tasks.
        Use the following pieces of retrieved CONTEXT to answer the QUESTION.
        If you don't know the answer, just say that you don't know.
        ---------------------
        CONTEXT: {context}
        ---------------------
        Given this information, please answer the QUESTION: {query}.
        """
        prompt = PromptTemplate.from_template(template)
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        
        chain = (
            {
                "context": retriever.with_config(run_name="Docs"),
                "query": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return chain
    except Exception as e:
        st.error(f"Error initializing RAG pipeline: {e}")
        return None

user_query = st.chat_input("Ask a question about the Build with AI Udaipur event")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        chain = initialize_rag_pipeline()
        
        if chain:
            response = ""
            message_placeholder = st.empty()
            
            with st.spinner("Generating response..."):
                for chunk in chain.stream(user_query):
                    response += chunk
                    message_placeholder.markdown(response + "▌")
                message_placeholder.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Failed to initialize RAG pipeline. Check your secrets.toml file and vector database.")
