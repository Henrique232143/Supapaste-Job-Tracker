from difflib import SequenceMatcher

from .models import Empresa, normalizar_nome_empresa_base


def encontrar_empresas_semelhantes(
    nome,
    limite=0.78,
    quantidade=5
):
    """
    Procura empresas que tenham nomes semelhantes
    ao nome informado.

    Retorna uma lista de tuplas:
    (empresa, percentual_de_similaridade)
    """

    nome_base = normalizar_nome_empresa_base(nome)

    if not nome_base:
        return []

    resultados = []

    for empresa in Empresa.objects.all():

        empresa_base = normalizar_nome_empresa_base(
            empresa.name
        )

        if not empresa_base:
            continue

        similaridade = SequenceMatcher(
            None,
            nome_base,
            empresa_base
        ).ratio()

        palavras_nome = nome_base.split()
        palavras_empresa = empresa_base.split()

        # Trata casos como:
        # "itau" x "itau unibanco"
        # "banco" x "banco do brasil"
        if (
            palavras_nome
            and palavras_empresa
            and palavras_nome[0] == palavras_empresa[0]
            and len(palavras_nome[0]) >= 4
        ):
            similaridade = max(
                similaridade,
                0.88
            )

        if similaridade >= limite:

            resultados.append(
                (
                    empresa,
                    round(similaridade * 100, 1)
                )
            )

    resultados.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return resultados[:quantidade]