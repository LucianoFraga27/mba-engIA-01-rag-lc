# Ingestão e Busca Semântica com LangChain e Gemini

Este projeto utiliza RAG para responder perguntas sobre um documento PDF, usando LangChain, Gemini e um banco de dados vetorial com PostgreSQL e pgVector. **[Task](prompt.md)**.

Para um passo a passo detalhado sobre a lógica e o desenvolvimento do projeto, acesse o **[Tutorial de Desenvolvimento](tutorial.md)**.

## Como Executar o Projeto

### 1. Pré-requisitos
- Docker e Docker Compose
- Python 3.9+
- Uma chave de API do Google

### 2. Configuração Rápida

**a. Clone o repositório e instale as dependências:**
```bash
# Clone o projeto (se ainda não o fez)
git clone <url-do-repositorio>
cd <pasta-do-projeto>

# Instale as dependências
pip install -r requirements.txt
```

**b. Configure o arquivo `.env`:**

Copie o `.env.example` para um novo arquivo chamado `.env` e preencha com suas informações (chave de API do Google, etc.).

### 3. Ordem de Execução

**a. Inicie o Banco de Dados:**
```bash
docker compose up -d
```

**b. Processe e Ingeria o PDF:**
```bash
python src/ingest.py
```

**c. Inicie o Chat para Perguntas:**
```bash
python src/chat.py
```