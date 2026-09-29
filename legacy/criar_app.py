import subprocess
import sys

nome_app = "empresas"

print(f"Criando aplicação Django: {nome_app}...\n")

try:
    subprocess.run(
        [
            sys.executable,
            "manage.py",
            "startapp",
            nome_app
        ],
        check=True
    )

    print(f"\nAplicação '{nome_app}' criada com sucesso!")

except subprocess.CalledProcessError:
    print("\nErro ao criar a aplicação.")