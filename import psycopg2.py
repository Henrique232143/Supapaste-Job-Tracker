import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# CONEXÃO COM O BANCO
# =========================

def conectar_banco():
    return psycopg2.connect(
        os.getenv("DATABASE_URL")
    )


# =========================
# CADASTRAR EMPRESA
# =========================

def cadastrar_empresa():
    conn = conectar_banco()
    cursor = conn.cursor()

    nome = input("Nome da empresa: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    website = input("Website: ")

    sql = """
    INSERT INTO companies (name, city, state, website)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cidade, estado, website))

    conn.commit()

    print("\nEmpresa cadastrada com sucesso!")

    cursor.close()
    conn.close()


# =========================
# LISTAR EMPRESAS
# =========================

def listar_empresas():
    conn = conectar_banco()
    cursor = conn.cursor()

    sql = """
    SELECT id, name, city, state, website
    FROM companies
    ORDER BY id
    """

    cursor.execute(sql)

    empresas = cursor.fetchall()

    print("\n===== EMPRESAS CADASTRADAS =====")

    if not empresas:
        print("Nenhuma empresa cadastrada.")

    for empresa in empresas:
        id, nome, cidade, estado, website = empresa

        print(f"""
ID: {id}
Nome: {nome}
Cidade: {cidade} - {estado}
Website: {website}
-------------------------------
""")

    cursor.close()
    conn.close()


# =========================
# BUSCAR EMPRESA POR ID
# =========================

def buscar_empresa():
    conn = conectar_banco()
    cursor = conn.cursor()

    id_empresa = input("Digite o ID da empresa: ")

    sql = """
    SELECT id, name, city, state, website
    FROM companies
    WHERE id = %s
    """

    cursor.execute(sql, (id_empresa,))

    empresa = cursor.fetchone()

    if empresa:
        id, nome, cidade, estado, website = empresa

        print("\n===== EMPRESA ENCONTRADA =====")
        print(f"ID: {id}")
        print(f"Nome: {nome}")
        print(f"Cidade: {cidade}")
        print(f"Estado: {estado}")
        print(f"Website: {website}")

    else:
        print("\nEmpresa não encontrada.")

    cursor.close()
    conn.close()


# =========================
# ATUALIZAR EMPRESA
# =========================

def atualizar_empresa():
    conn = conectar_banco()
    cursor = conn.cursor()

    id_empresa = input("Digite o ID da empresa que deseja atualizar: ")

    cursor.execute(
        """
        SELECT id, name, city, state, website
        FROM companies
        WHERE id = %s
        """,
        (id_empresa,)
    )

    empresa = cursor.fetchone()

    if not empresa:
        print("\nEmpresa não encontrada.")
        cursor.close()
        conn.close()
        return

    print("\nEmpresa encontrada:")
    print(f"Nome: {empresa[1]}")
    print(f"Cidade: {empresa[2]}")
    print(f"Estado: {empresa[3]}")
    print(f"Website: {empresa[4]}")

    print("\nDigite os novos dados:")

    nome = input("Nome: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    website = input("Website: ")

    sql = """
    UPDATE companies
    SET name = %s,
        city = %s,
        state = %s,
        website = %s
    WHERE id = %s
    """

    cursor.execute(
        sql,
        (nome, cidade, estado, website, id_empresa)
    )

    conn.commit()

    print("\nEmpresa atualizada com sucesso!")

    cursor.close()
    conn.close()


# =========================
# EXCLUIR EMPRESA
# =========================

def excluir_empresa():
    conn = conectar_banco()
    cursor = conn.cursor()

    id_empresa = input("Digite o ID da empresa que deseja excluir: ")

    cursor.execute(
        """
        SELECT id, name, city, state, website
        FROM companies
        WHERE id = %s
        """,
        (id_empresa,)
    )

    empresa = cursor.fetchone()

    if not empresa:
        print("\nEmpresa não encontrada.")
        cursor.close()
        conn.close()
        return

    print("\nEmpresa encontrada:")
    print(f"ID: {empresa[0]}")
    print(f"Nome: {empresa[1]}")
    print(f"Cidade: {empresa[2]}")
    print(f"Estado: {empresa[3]}")
    print(f"Website: {empresa[4]}")

    confirmacao = input("\nTem certeza que deseja excluir? (s/n): ")

    if confirmacao.lower() == "s":

        cursor.execute(
            "DELETE FROM companies WHERE id = %s",
            (id_empresa,)
        )

        conn.commit()

        print("\nEmpresa excluída com sucesso!")

    else:
        print("\nExclusão cancelada.")

    cursor.close()
    conn.close()


# =========================
# MENU PRINCIPAL
# =========================

def menu():

    while True:

        print("""
==============================
          SUPAPASTE
==============================

1 - Cadastrar empresa
2 - Listar empresas
3 - Buscar empresa por ID
4 - Atualizar empresa
5 - Excluir empresa
0 - Sair

==============================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_empresa()

        elif opcao == "2":
            listar_empresas()

        elif opcao == "3":
            buscar_empresa()

        elif opcao == "4":
            atualizar_empresa()

        elif opcao == "5":
            excluir_empresa()

        elif opcao == "0":
            print("\nSaindo do Supapaste...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


# =========================
# INICIAR PROGRAMA
# =========================

menu()