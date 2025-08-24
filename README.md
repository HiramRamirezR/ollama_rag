# Ollama RAG Project

## Description

This project implements a Retrieval-Augmented Generation (RAG) system to chat with your PDF documents locally. It uses Ollama to run the `gemma3:270m` language model, ChromaDB for the vector store, and LangChain to orchestrate the process.

This version includes a Discord bot interface to interact with your documents.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/HiramRamirezR/ollama_rag.git
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

### Step 1: Ingest Your Document

Before using the bot, you must process your PDF document. This creates the local vector store that the bot will use to answer questions.

1.  Place your PDF document in the project's root directory.
2.  Run the `app.py` script, passing the path to your PDF as an argument:
    ```bash
    python app.py your-document.pdf
    ```
3.  The script will process the document and create a local vector store in the `./local_knowledge_db` directory. You only need to do this once per document.

### Step 2: Run the Discord Bot

1.  **Set up your Discord Token:** The bot requires a `DISCORD_TOKEN` to log in. For security, set it as an environment variable.
    
    *   On Windows (Command Prompt):
        ```cmd
        set DISCORD_TOKEN="your_discord_token_here"
        ```
    *   On Windows (PowerShell):
        ```powershell
        $env:DISCORD_TOKEN="your_discord_token_here"
        ```
    *   On Linux/macOS:
        ```bash
        export DISCORD_TOKEN="your_discord_token_here"
        ```
2.  **Run the bot:**
    ```bash
    python discord_bot.py
    ```
3.  Once the bot is running, it will print a confirmation message to your terminal.

### Step 3: Interact with the Bot in Discord

1.  Invite the bot to your Discord server.
2.  In any channel the bot has access to, type `!ask` followed by your question. For example:
    ```
    !ask What is the main topic of the document?
    ```
3.  The bot will process the question and send the answer back to the channel, including the page numbers from the document that were used as sources.

## Dependencies

The project uses the following Python libraries:

*   `langchain`
*   `langchain_community`
*   `langchain_ollama`
*   `langchain_chroma`
*   `chromadb`
*   `pypdf`
*   `fastembed`
*   `discord.py`

You can install them all with `pip install -r requirements.txt`.