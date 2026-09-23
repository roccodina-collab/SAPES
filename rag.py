from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Inicialitzar el model d'embeddings local (gratuït)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Inicialitzar o carregar la DB local
vector_db = Chroma(
    persist_directory="./data/chromadb",
    embedding_function=embedding_function,
    collection_name="project_knowledge"
)

def query_knowledge_base(query: str, k: int = 3) -> str:
    """Cerca informació rellevant en la base de dades de coneixement local."""
    results = vector_db.similarity_search(query, k=k)
    if not results:
        return "No s'ha trobat informació rellevant al RAG."
    return "\n---\n".join([doc.page_content for doc in results])