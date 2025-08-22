from langchain_community.document.loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Process PDF document and create vectorial base
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