# Book Chat

A simple application that allows you to chat with your PDF documents using local LLMs through Ollama.

## Features

- Upload and process PDF documents
- Ask questions about the document content
- Uses local LLM (Ollama) for responses
- Fast text extraction with PyMuPDF
- Efficient vector storage with ChromaDB

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- Ollama model (llama2) pulled and ready to use

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd book-chat
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (usually http://localhost:8501)

3. In the app:
   - Upload a PDF file
   - Click "Process PDF" to process the document
   - Once processed, you can ask questions about the content

## Dependencies

- streamlit
- langchain-community>=0.0.28
- langchain-core==0.1.31
- pymupdf==1.25.5
- chromadb==0.4.24
- python-dotenv==1.0.1
- huggingface-hub==0.22.2
- sentence-transformers==2.5.1
- ollama==0.1.6

## Notes

- Make sure Ollama is running before starting the app
- The first run might take longer as it downloads the required models
- Processing large PDFs might take some time depending on your system 