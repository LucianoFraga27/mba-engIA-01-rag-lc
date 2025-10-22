import os
from dotenv import load_dotenv

load_dotenv()

# 4.1 Valida as variáveis de ambiente
def validateEnvs():
    """Verifica se todas as variáveis de ambiente obrigatórias estão definidas."""
    print("Verificando variáveis de ambiente obrigatórias...")
    required_vars = [
        "GOOGLE_API_KEY", 
        "DATABASE_URL", 
        "PG_VECTOR_COLLECTION_NAME",
        "GOOGLE_EMBEDDING_MODEL",
        "GOOGLE_CHAT_MODEL"
    ]
    for k in required_vars:
        if not os.getenv(k):
            raise RuntimeError(f"A variável de ambiente {k} não está definida.")
    print("Variáveis de ambiente verificadas com sucesso.")
