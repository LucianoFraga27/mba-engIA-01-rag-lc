from dotenv import load_dotenv
from search import search_prompt

load_dotenv()
# 3.1 Função principal do chat
def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("--- Chat Iniciado ---")
    print('Digite "sair" para encerrar.')

    while True:
        question = input("\nFaça sua pergunta: ")

        if question.lower() == "sair":
            print("Encerrando o chat.")
            break

        if not question.strip():
            print("Por favor, digite uma pergunta.")
            continue

        response = chain.invoke(question)
        print(f"\nRESPOSTA: {response}")

if __name__ == "__main__":
    main()
