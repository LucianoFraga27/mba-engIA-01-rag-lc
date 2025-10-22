
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

# 2.1 Inicializa a cadeia de busca e resposta
def search_prompt():
    """
    Inicializa e retorna uma cadeia de processamento (chain) para busca e resposta.
    """
    try:
        embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL")
        chat_model = os.getenv("GOOGLE_CHAT_MODEL")

        print(f"Usando embedding model: {embedding_model}")
        print(f"Usando chat model: {chat_model}")

        embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        
        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )
        retriever = store.as_retriever(search_kwargs={'k': 10})
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        
        llm = GoogleGenerativeAI(model=chat_model, temperature=0)

        # 2.2 Formata os documentos recuperados para o prompt
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        print("Chat pronto para receber perguntas.")
        return chain

    except Exception as e:
        print(f"Erro ao inicializar o search_prompt: {e}")
        return None
