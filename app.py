from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import sys

# Process PDF document and create vector base
def ingest_document(pdf_path):
    print("Loading your document...")

    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1024,
        chunk_overlap = 100,
        length_function = len,
        add_start_index = True
    )

    chunks = text_splitter.split_documents(pages)

    print(f"Converted {len(pages)} pages into {len(chunks)} smart chunks.")

    embedding = FastEmbedEmbeddings()

    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embedding,
        persist_directory = "./local_knowledge_db"
    )

    print("Your local AI already knows the document.")
    return vector_store

# Create RAG to interact with documents
def create_local_rag_chain():
    local_llm = ChatOllama(
        model = "gemma3:270m",
        temperature = 0.7
    )

    prompt_template = PromptTemplate.from_template(
        """
        You are an intelligent and expert assistant.
        Answer based on the provided context of the documents.

        If you don't find the information in the context, say so clearly.
        Always mention which part of the document your answer comes from.

        Document context:
        {context}

        User question:
        {input}

        Detailed answer:
        """ # noqa: F541
    )

    embedding = FastEmbedEmbeddings()
    vector_store = Chroma(
        persist_directory = "./local_knowledge_db",
        embedding_function = embedding
    )

    # Use the default retriever which is more lenient and effective.
    retriever = vector_store.as_retriever()

    document_chain = create_stuff_documents_chain(local_llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain

# Chat with document
def chat_whit_document(chain, question):
    print(f"Question: {question}")
    print("Looking in the document...")

    result = chain.invoke({"input": question})

    print(f"Answer: \n{result["answer"]}")
    if result["context"]:
        print("\n Sources:")
        for i, doc in enumerate(result["context"], 1):
            page_num = doc.metadata.get("page")
            print(f"{i}. Page {page_num + 1 if isinstance(page_num, int) else '?'} of document")

    return result

# System interaction
def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <path_to_pdf>")
        print("Please provide the path to your PDF document as an argument.")
        return

    print("Starting local AI with RAG...")

    # Document path
    pdf_path = sys.argv[1]
    ingest_document(pdf_path)

    print("Document ingestion complete.")

if __name__ == "__main__":
    main()