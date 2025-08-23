# Ollama RAG Project

## Description

This project implements a Retrieval-Augmented Generation (RAG) system to chat with your PDF documents locally. It uses Ollama to run the `gemma3:270m` language model, ChromaDB for the vector store, and LangChain to orchestrate the process.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/ollama-rag.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Make sure you have Ollama installed and the `gemma3:270m` model pulled:
    ```bash
    ollama pull gemma3:270m
    ```

## Usage

1.  Place your PDF document in the project's root directory.
2.  Run the `app.py` script, passing the path to your PDF as an argument:
    ```bash
    python app.py your-document.pdf
    ```
3.  The script will process the document and create a local vector store in the `./local_knowledge_db` directory.
4.  Once the document is processed, you can interact with the RAG chain to ask questions about your document in the terminal.
5.  Type your question and press Enter. The script will print the answer and the page numbers from the document that were used as sources.
6.  To end the chat, type `exit` and press Enter.

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