# Ollama RAG Project

## Description

This project implements a Retrieval-Augmented Generation (RAG) system to chat with your PDF documents locally. It uses Ollama to run the language model, ChromaDB for the vector store, and LangChain to orchestrate the process.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/ollama-rag.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Make sure you have Ollama installed and the `deepseek-r1` model pulled:
    ```bash
    ollama pull deepseek-r1
    ```

## Usage

1.  Place your PDF document in the project's root directory.
2.  Run the `app.py` script, passing the path to your PDF as an argument:
    ```bash
    python app.py your-document.pdf
    ```
3.  The script will process the document and create a local vector store in the `./local_knowledge_db` directory.
4.  You can then interact with the RAG chain to ask questions about your document.

## Dependencies

The project uses the following Python libraries:

*   `langchain`
*   `langchain_community`
*   `langchain_ollama`
*   `langchain_chroma`
*   `chromadb`
*   `pypdf`
*   `fastembed`

You can install them all with `pip install -r requirements.txt`.

## Credit

This project is based on the tutorial from the following video:
[https://youtu.be/VyAbT4m48Ic?si=G4icPZ0D01clMNI7&t=1060](https://youtu.be/VyAbT4m48Ic?si=G4icPZ0D01clMNI7&t=1060)
