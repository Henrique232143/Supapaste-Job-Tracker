from empresas import (
    cadastrar_empresa,
    listar_empresas,
    buscar_empresa,
    atualizar_empresa,
    excluir_empresa
)


def menu():

    while True:

        print("""
==============================
          SUPAPASTE
==============================

1 - Cadastrar empresa
2 - Listar empresas
3 - Buscar empresa
4 - Atualizar empresa
5 - Excluir empresa
0 - Sair

==============================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\nAbrindo o menu de cadastro...")
            cadastrar_empresa()

        elif opcao == "2":
            print("\nListando empresas...")
            listar_empresas()

        elif opcao == "3":
            print("\nAbrindo o menu de buscas...")
            buscar_empresa()

        elif opcao == "4":
            print("\nAbrindo o menu de atualização...")
            atualizar_empresa()

        elif opcao == "5":
            print("\nAbrindo o menu de exclusão...")
            excluir_empresa()

        elif opcao == "0":
            print("\nDeslogando do Sistema ...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


menu()