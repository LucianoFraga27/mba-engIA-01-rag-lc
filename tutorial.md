# Tutorial de Desenvolvimento

Este documento detalha o processo de desenvolvimento e a lógica por trás de cada componente do sistema de ingestão e busca semântica.

## Objetivo do Projeto

O objetivo era criar uma aplicação de linha de comando (CLI) capaz de "ler" um documento PDF e responder perguntas sobre seu conteúdo, sem utilizar conhecimento externo. Para isso, usamos a técnica de RAG (Retrieval-Augmented Generation).

---

## Ordem de Execução e Fluxo do Projeto

O projeto segue um fluxo lógico para ingestão de dados e, posteriormente, para a interação via chat. As funções são numeradas para facilitar a referência:

1.  **`src/ingest.py`**: Responsável por processar o PDF e armazenar os embeddings no banco de dados.
    *   **1.7 `main()`**: Orquestra o pipeline de ingestão.
        *   **4.1 `validateEnvs()`** (de `src/utils.py`): Garante que as variáveis de ambiente necessárias estejam configuradas.
        *   **1.1 `carregar_pdf()`**: Carrega o documento PDF.
        *   **1.2 `dividir_em_chunks()`**: Divide o conteúdo do PDF em trechos menores.
        *   **1.3 `limpar_metadados()`**: Limpa e estrutura os metadados dos chunks.
        *   **1.4 `gerar_ids()`**: Gera identificadores únicos para cada chunk.
        *   **1.5 `inicializar_embeddings()`**: Inicializa o modelo de embeddings do Gemini.
        *   **1.6 `salvar_no_pgvector()`**: Salva os chunks e seus embeddings no PostgreSQL com pgVector.

2.  **`src/chat.py`**: A interface de linha de comando para interação com o usuário.
    *   **3.1 `main()`**: Ponto de entrada do chat.
        *   **2.1 `search_prompt()`** (de `src/search.py`): Inicializa a cadeia de busca e resposta.
            *   **2.2 `format_docs()`**: Função auxiliar para formatar os documentos recuperados.

---

## Passo 1: Estrutura Inicial e Ambiente

O desenvolvimento começou com uma estrutura de projeto pré-definida, contendo os arquivos principais e as configurações de ambiente.

1.  **`docker-compose.yml`**: Define o serviço do banco de dados PostgreSQL com a extensão `pgvector`, essencial para armazenar e consultar vetores de embeddings de forma eficiente.
2.  **`.env.example`**: Um arquivo modelo para as variáveis de ambiente. Centralizar as configurações (chaves de API, URLs de banco de dados, nomes de modelos) aqui torna o código mais limpo e seguro.
3.  **`requirements.txt`**: Lista as dependências Python do projeto, como `langchain`, `psycopg2-binary`, `langchain-google-genai`, etc.

## Passo 2: A Lógica de Ingestão (`src/ingest.py`)

O primeiro desafio de código foi ensinar o programa a ler e armazenar o conhecimento do PDF. As funções numeradas correspondem aos métodos em `src/ingest.py`.

*   **1.1 `carregar_pdf()`**: Carrega o conteúdo do PDF e retorna uma lista de documentos LangChain (um por página).
*   **1.2 `dividir_em_chunks()`**: Divide os documentos em trechos menores (chunks) para processamento vetorial.
*   **1.3 `limpar_metadados()`**: Remove metadados vazios e cria instâncias limpas de Document.
*   **1.4 `gerar_ids()`**: Gera identificadores únicos para os documentos.
*   **1.5 `inicializar_embeddings()`**: Inicializa o modelo de embeddings do Google Gemini.
*   **1.6 `salvar_no_pgvector()`**: Salva os documentos e seus embeddings no PostgreSQL usando PGVector.

## Passo 3: A Lógica de Busca e Resposta (`src/search.py`)

Uma vez que o conhecimento está no banco, o próximo passo é criar a lógica para consultá-lo. As funções numeradas correspondem aos métodos em `src/search.py`.

*   **2.1 `search_prompt()`**: Inicializa e retorna uma cadeia de processamento (chain) para busca e resposta.
*   **2.2 `format_docs()`**: Função auxiliar que formata os documentos recuperados do banco de dados para serem inseridos no prompt do LLM.

## Passo 4: Interface do Usuário (`src/chat.py`)

Este é o ponto de entrada para o usuário final. A função numerada corresponde ao método em `src/chat.py`.

*   **3.1 `main()`**: A função principal que gerencia o loop de interação com o usuário no terminal.

## Passo 5: Validação e Configuração (`src/utils.py`)

Para garantir a robustez, foram tomados alguns cuidados. A função numerada corresponde ao método em `src/utils.py`.

*   **4.1 `validateEnvs()`**: Verifica se todas as variáveis de ambiente obrigatórias foram definidas antes de o programa tentar executá-las, evitando erros em tempo de execução.
