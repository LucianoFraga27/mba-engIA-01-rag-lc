import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

from utils import validateEnvs

# Carregamento de variáveis de ambiente
load_dotenv()
PDF_PATH = os.getenv("PDF_PATH")

# 1.1 Carregamento do PDF
def carregar_pdf(pdf_path: str):
    """Carrega o conteúdo do PDF e retorna uma lista de documentos LangChain (um por página)."""
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"O caminho PDF_PATH '{pdf_path}' é inválido ou não existe.")

    print(f"Carregando documento PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"{len(docs)} páginas carregadas com sucesso.")

    for i, doc in enumerate(docs):
        texto_preview = doc.page_content[:120].replace("\n", " ")
        print(f"[Página {i+1}] {len(doc.page_content)} caracteres - prévia: {texto_preview}...")
    return docs



# 1.2 Divisão dos documentos em trechos (chunks)
def dividir_em_chunks(docs, chunk_size=1000, chunk_overlap=150):
    """Divide os documentos em trechos menores (chunks) para processamento vetorial."""
    print("Dividindo as páginas em trechos menores...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)

    if not chunks:
        print("Nenhum trecho foi gerado. Verifique se o PDF contém texto extraível.")
        raise SystemExit(0)

    print(f"Total de {len(chunks)} trechos gerados.")
    for i, chunk in enumerate(chunks[:5]):  # mostra os 5 primeiros
        preview = chunk.page_content[:120].replace("\n", " ")
        print(f"Trecho {i+1}: {len(chunk.page_content)} caracteres - prévia: {preview}...")
    return chunks



# 1.3 Limpeza de metadados
def limpar_metadados(chunks):
    """Remove metadados vazios e cria instâncias limpas de Document."""
    print("Limpando metadados e estruturando documentos...")
    enriched = []

    for chunk in chunks:
        metadata_limpa = {k: v for k, v in chunk.metadata.items() if v not in ("", None)}
        document = Document(page_content=chunk.page_content.strip(), metadata=metadata_limpa)
        enriched.append(document)

    print(f"{len(enriched)} documentos prontos para armazenamento.")
    return enriched



# 1.4 Geração de identificadores únicos
def gerar_ids(enriched):
    """Gera identificadores únicos para os documentos."""
    ids = [f"doc-{i}" for i in range(len(enriched))]
    print(f"{len(ids)} identificadores gerados para os documentos.")
    return ids


# 1.5 Inicialização do modelo de embeddings
def inicializar_embeddings():
    """Inicializa o modelo de embeddings do Google Gemini."""
    model_name = os.getenv("GEMINI_EMBEDDING_MODEL")
    print(f"Inicializando embeddings com o modelo: {model_name}")
    return GoogleGenerativeAIEmbeddings(model=model_name)


# 1.6 Persistência dos documentos no PostgreSQL (pgvector)
def salvar_no_pgvector(embeddings, enriched, ids):
    """Salva os documentos e seus embeddings no PostgreSQL usando PGVector."""
    pg_collection = os.getenv("PG_VECTOR_COLLECTION_NAME")
    database_url = os.getenv("DATABASE_URL")
    print("Estabelecendo conexão com o banco PostgreSQL.")
    print(f"Collection name: {pg_collection}")
    print(f"Database URL: {database_url}")
    store = PGVector(
        embeddings=embeddings,
        collection_name=pg_collection,
        connection=database_url,
        use_jsonb=True,
    )
    print("Iniciando inserção dos documentos na base vetorial...")
    store.add_documents(documents=enriched, ids=ids)
    print("Documentos inseridos com sucesso.")
    
# 1.7 Pipeline principal de ingestão
def main():
    validateEnvs()
    print("Iniciando processo completo de ingestão do PDF.")
    docs = carregar_pdf(PDF_PATH)
    chunks = dividir_em_chunks(docs, chunk_size=1000, chunk_overlap=150)
    enriched = limpar_metadados(chunks)
    ids = gerar_ids(enriched)
    embeddings = inicializar_embeddings()
    salvar_no_pgvector(embeddings, enriched, ids)
    print("Processo de ingestão concluído com êxito.")


if __name__ == "__main__":
    main()
