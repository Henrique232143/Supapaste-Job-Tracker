import subprocess
import sys

print("Aplicando migrations do Django...\n")

try:
    subprocess.run(
        [
            sys.executable,
            "manage.py",
            "migrate"
        ],
        check=True
    )

    print("\nMigrations aplicadas com sucesso!")

except subprocess.CalledProcessError:
    print("\nErro ao aplicar as migrations.")