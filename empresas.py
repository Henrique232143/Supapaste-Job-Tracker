import re

from database import conectar_banco


# =========================
# FUNÇÕES DE VALIDAÇÃO
# =========================

def pedir_texto(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("Esse campo não pode ficar vazio.")


def pedir_id(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor.isdigit():
            return int(valor)

        print("Digite apenas números.")


def pedir_estado(mensagem):
    estados_validos = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF",
        "ES", "GO", "MA", "MT", "MS", "MG", "PA",
        "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
        "RO", "RR", "SC", "SP", "SE", "TO"
    }

    while True:
        estado = input(mensagem).strip().upper()

        if estado in estados_validos:
            return estado

        print(
            "Estado inválido. Digite uma UF brasileira válida. "
            "Exemplo: DF"
        )


def pedir_website(mensagem):
    while True:
        website = input(mensagem).strip()

        if re.match(r"^https?://", website):
            return website

        print(
            "Digite um website válido começando com "
            "http:// ou https://"
        )


# =========================
# CADASTRAR EMPRESA
# =========================

def cadastrar_empresa():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        nome = pedir_texto("Nome da empresa: ")
        cidade = pedir_texto("Cidade: ")
        estado = pedir_estado("Estado: ")
        website = pedir_website("Website: ")

        sql = """
        INSERT INTO companies (name, city, state, website)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """

        cursor.execute(
            sql,
            (nome, cidade, estado, website)
        )

        id_empresa = cursor.fetchone()[0]

        conn.commit()

        print("\nEmpresa cadastrada com sucesso!")
        print(f"ID gerado: {id_empresa}")

    except Exception as erro:

        conn.rollback()

        print("\nErro ao cadastrar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# LISTAR EMPRESAS
# =========================

def listar_empresas():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

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
            return

        for empresa in empresas:

            id, nome, cidade, estado, website = empresa

            print(f"""
ID: {id}
Nome: {nome}
Cidade: {cidade} - {estado}
Website: {website}
-------------------------------
""")

    except Exception as erro:

        print("\nErro ao listar empresas.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# MENU DE BUSCA
# =========================

def buscar_empresa():

    while True:

        print("""
===== BUSCAR EMPRESA =====

1 - Buscar por ID
2 - Buscar por nome
3 - Buscar por cidade
4 - Buscar por estado
0 - Voltar
""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":

            buscar_por_id()

        elif opcao == "2":

            buscar_por_nome()

        elif opcao == "3":

            buscar_por_cidade()

        elif opcao == "4":

            buscar_por_estado()

        elif opcao == "0":

            return

        else:

            print("\nOpção inválida.")


# =========================
# BUSCAR POR ID
# =========================

def buscar_por_id():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        id_empresa = pedir_id(
            "Digite o ID da empresa: "
        )

        sql = """
        SELECT id, name, city, state, website
        FROM companies
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (id_empresa,)
        )

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

    except Exception as erro:

        print("\nErro ao buscar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# BUSCAR POR NOME
# =========================

def buscar_por_nome():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        nome = pedir_texto(
            "Digite o nome da empresa: "
        )

        sql = """
        SELECT id, name, city, state, website
        FROM companies
        WHERE name ILIKE %s
        ORDER BY name
        """

        cursor.execute(
            sql,
            (f"%{nome}%",)
        )

        empresas = cursor.fetchall()

        print("\n===== RESULTADOS =====")

        if not empresas:

            print("Nenhuma empresa encontrada.")
            return

        for empresa in empresas:

            id, nome, cidade, estado, website = empresa

            print(f"""
ID: {id}
Nome: {nome}
Cidade: {cidade} - {estado}
Website: {website}
-------------------------------
""")

    except Exception as erro:

        print("\nErro ao buscar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# BUSCAR POR CIDADE
# =========================

def buscar_por_cidade():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        cidade = pedir_texto(
            "Digite a cidade: "
        )

        sql = """
        SELECT id, name, city, state, website
        FROM companies
        WHERE city ILIKE %s
        ORDER BY name
        """

        cursor.execute(
            sql,
            (f"%{cidade}%",)
        )

        empresas = cursor.fetchall()

        print("\n===== EMPRESAS ENCONTRADAS =====")

        if not empresas:

            print("Nenhuma empresa encontrada.")
            return

        for empresa in empresas:

            id, nome, cidade, estado, website = empresa

            print(f"""
ID: {id}
Nome: {nome}
Cidade: {cidade} - {estado}
Website: {website}
-------------------------------
""")

    except Exception as erro:

        print("\nErro ao buscar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# BUSCAR POR ESTADO
# =========================

def buscar_por_estado():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        estado = pedir_estado(
            "Digite o estado (UF): "
        )

        sql = """
        SELECT id, name, city, state, website
        FROM companies
        WHERE state = %s
        ORDER BY name
        """

        cursor.execute(
            sql,
            (estado,)
        )

        empresas = cursor.fetchall()

        print("\n===== EMPRESAS ENCONTRADAS =====")

        if not empresas:

            print("Nenhuma empresa encontrada.")
            return

        for empresa in empresas:

            id, nome, cidade, estado, website = empresa

            print(f"""
ID: {id}
Nome: {nome}
Cidade: {cidade} - {estado}
Website: {website}
-------------------------------
""")

    except Exception as erro:

        print("\nErro ao buscar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# ATUALIZAR EMPRESA
# =========================

def atualizar_empresa():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        id_empresa = pedir_id(
            "Digite o ID da empresa que deseja atualizar: "
        )

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
            return

        print("\nEmpresa encontrada:")
        print(f"Nome: {empresa[1]}")
        print(f"Cidade: {empresa[2]}")
        print(f"Estado: {empresa[3]}")
        print(f"Website: {empresa[4]}")

        print("\nDigite os novos dados:")

        nome = pedir_texto("Nome: ")
        cidade = pedir_texto("Cidade: ")
        estado = pedir_estado("Estado: ")
        website = pedir_website("Website: ")

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

    except Exception as erro:

        conn.rollback()

        print("\nErro ao atualizar empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()


# =========================
# EXCLUIR EMPRESA
# =========================

def excluir_empresa():

    conn = conectar_banco()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        id_empresa = pedir_id(
            "Digite o ID da empresa que deseja excluir: "
        )

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
            return

        print("\nEmpresa encontrada:")
        print(f"ID: {empresa[0]}")
        print(f"Nome: {empresa[1]}")
        print(f"Cidade: {empresa[2]}")
        print(f"Estado: {empresa[3]}")
        print(f"Website: {empresa[4]}")

        confirmacao = input(
            "\nTem certeza que deseja excluir? (s/n): "
        ).strip().lower()

        if confirmacao == "s":

            cursor.execute(
                "DELETE FROM companies WHERE id = %s",
                (id_empresa,)
            )

            conn.commit()

            print("\nEmpresa excluída com sucesso!")

        elif confirmacao == "n":

            print("\nExclusão cancelada.")

        else:

            print("\nOpção inválida. Exclusão cancelada.")

    except Exception as erro:

        conn.rollback()

        print("\nErro ao excluir empresa.")
        print(f"Detalhes: {erro}")

    finally:

        cursor.close()
        conn.close()