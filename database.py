import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def conectar_banco():
    try:
        return psycopg2.connect(
            os.getenv("DATABASE_URL")
        )

    except psycopg2.Error as erro:
        print("\nErro ao conectar ao banco de dados.")
        print(f"Detalhes: {erro}")
        return None