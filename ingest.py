import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def ingest_folder():
    # Detecta si existeix una subcarpeta SAPES o si la carpeta actual és la principal
    target_dir = "./SAPES" if os.path.exists("./SAPES") else "."
    print(f"📂 Carregant fitxers des de '{os.path.abspath(target_dir)}'...")

    # Directoris a ignorar per no carregar dependències ni la base de dades
    exclude_dirs = {"venv", ".git", "data", "__pycache__", ".github"}
    documents = []

    for root, dirs, files in os.walk(target_dir):
        # Excloure les carpetes no desitjades
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            # Seleccionar fitxers de text, markdown o codi
            if file.endswith(('.txt', '.md', '.py', '.json', '.js', '.html', '.java')):
                if file in ["ingest.py", "main.py"]:
                    continue
                file_path = os.path.join(root, file)
                try:
                    loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"⚠️ Ometent fitxer {file_path}: {e}")

    if not documents:
        print("⚠️ No s'han trobat fitxers vàlids per indexar.")
        return

    print(f"📄 S'han trobat {len(documents)} document(s). Dividint el text en fragments...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    print(f"🧠 Generant embeddings per a {len(chunks)} fragments a ChromaDB...")
    
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory="./data/chromadb",
        collection_name="project_knowledge"
    )
    
    print("✅ Indexació finalitzada amb èxit! L'agent ja pot utilitzar aquesta informació.")

if __name__ == "__main__":
    ingest_folder()