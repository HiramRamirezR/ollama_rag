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

    print(f"Converted {len(pages)} pages in {len(chunks)} smart pieces.")

    embedding = FastEmbedEmbeddings()

    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embedding,
        persist_directory = "./local_knowledge_db"
    )

    print("Your local IA already knows the document.")
    return vector_store

# Create RAG to interact with documents
def create_local_rag_chain():
    local_llm = ChatOllama(
        model = "deepseek-r1",
        temperature = 0.7
    )

    prompt_template = PromptTemplate.from_template(
        f"""
        Eres un asistente inteligente y experto.
        Responde basándote en el contexto propocionado de los docuemntos.

        Si no encuentras la información en el contexto, dilo claramente.
        Siempre menciona de qué parte del documento viene tu respuesta.

        Contexto de los docuemntos:
        {context}

        Pregunta del usuario:
        {input}

        Respuesta detallada:
        """
    )

    embedding = FastEmbedEmbeddings()
    vector_store = Chroma(
        persist_directory = "./local_knowledge_db",
        embedding_funcion = embedding
    )

    retriever = vector_store.as_retriever(
        search_type = "similarity_score_threshold",
        search_kwargs = {"k": 3, "score_threshold": 0.5}
    )

    document_chain = create_stuff_documents_chain(local_llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain

# https://youtu.be/VyAbT4m48Ic?si=G4icPZ0D01clMNI7&t=1060