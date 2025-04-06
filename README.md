# build-with-ai-udaipur

Build a multi-document RAG using Gemini 2.0 and Qdrant via Langchain.

## Overview

This project demonstrates how to create a RAG-based chatbot that:
1. Scrapes content from web pages
2. Processes and indexes the content using embeddings
3. Retrieves relevant information based on user queries
4. Generates answers using Google's Gemini model

## Project Structure

```
build-with-ai-udaipur/
├── ingest.py            # Script for processing and indexing documents
├── app.py               # Streamlit web application
├── buildwithai-udaipur/ # Directory containing the vector database
└── .streamlit/secrets.toml # Contains your API key (not committed to git)
```

## Prerequisites

- Python 3.8 or higher
- Google API key with access to Gemini models

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd build-with-ai-udaipur
   ```

2. Install required packages:
   ```bash
   pip install streamlit langchain langchain-community langchain-google-genai qdrant-client
   ```

3. Set up your secrets:
   Create a `.streamlit/secrets.toml` file with:
   ```toml
   GOOGLE_API_KEY = "your-google-api-key-here"
   ```

## Usage

### Step 1: Process and Index Documents

Run the ingest script to scrape web pages and create the vector index:

```bash
python ingest.py
```

### Step 2: Launch the Chatbot

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will automatically use the API key from your secrets file and connect to the pre-built vector index.

### Step 3: Ask Questions

Use the chat interface to ask questions about the Build with AI Udaipur event. The system will:
1. Search the indexed content for relevant information
2. Provide the context to the Gemini model
3. Generate and stream a response based on the retrieved context

## Customization

- Edit the URLs in `ingest.py` to index different web pages
- Modify the prompt template in `app.py` to change the assistant's behavior
- Adjust chunk size and overlap in `ingest.py` to optimize retrieval performance

## Deployment

To deploy this application:

1. Create a requirements.txt file:
   ```bash
   pip freeze > requirements.txt
   ```

2. Deploy to Streamlit Cloud:
   - Connect your repository to [Streamlit Cloud](https://share.streamlit.io/)
   - Add your Google API key to the Streamlit Cloud secrets management. Click on Settings- Go to Secrets -> Add your key
   - Deploy the application

## Troubleshooting

- If you get vector database errors, ensure you've run `ingest.py` first
- For API key issues, verify your key has access to Gemini models
- If the application fails to start, check your Python environment and package installations

## Acknowledgments

- Built with Google's Generative AI models
- Powered by LangChain and Qdrant
- Created for the [Build with AI Udaipur event](https://gdg.community.dev/events/details/google-gdg-cloud-udaipur-presents-build-with-ai-udaipur-hands-on-edition/)
