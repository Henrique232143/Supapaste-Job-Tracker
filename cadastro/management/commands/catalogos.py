from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cadastro.models import (
    Empresa,
    Cargo,
    Candidatura,
    normalizar_nome,
)


class Command(BaseCommand):

    help = (
        'Preenche o catálogo global de empresas e cargos '
        'a partir dos dados existentes.'
    )

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(
            'Verificando empresas existentes...'
        )

        empresas = Empresa.objects.all().order_by('id')

        empresas_normalizadas = {}

        for empresa in empresas:

            nome_normalizado = normalizar_nome(
                empresa.name
            )

            if nome_normalizado in empresas_normalizadas:

                empresa_anterior = empresas_normalizadas[
                    nome_normalizado
                ]

                raise CommandError(
                    '\nForam encontradas empresas duplicadas:\n\n'
                    f'- ID {empresa_anterior.id}: '
                    f'{empresa_anterior.name}\n'
                    f'- ID {empresa.id}: '
                    f'{empresa.name}\n\n'
                    'Corrija a duplicidade antes de continuar.'
                )

            empresas_normalizadas[
                nome_normalizado
            ] = empresa

        for empresa in empresas:

            empresa.name = " ".join(
                empresa.name.strip().split()
            )

            empresa.name_normalized = normalizar_nome(
                empresa.name
            )

            empresa.save(
                update_fields=[
                    'name',
                    'name_normalized',
                ]
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'{len(empresas)} empresa(s) processada(s).'
            )
        )

        self.stdout.write(
            'Criando catálogo de cargos...'
        )

        cargos_existentes = set(
            Cargo.objects.values_list(
                'name_normalized',
                flat=True
            )
        )

        cargos_candidaturas = (
            Candidatura.objects
            .exclude(cargo='')
            .values_list(
                'cargo',
                flat=True
            )
            .order_by('cargo')
        )

        cargos_criados = 0

        for nome_cargo in cargos_candidaturas:

            nome_cargo = " ".join(
                nome_cargo.strip().split()
            )

            nome_normalizado = normalizar_nome(
                nome_cargo
            )

            if not nome_normalizado:
                continue

            if nome_normalizado in cargos_existentes:
                continue

            Cargo.objects.create(
                name=nome_cargo,
                name_normalized=nome_normalizado
            )

            cargos_existentes.add(
                nome_normalizado
            )

            cargos_criados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{cargos_criados} cargo(s) criado(s).'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                '\nCatálogos atualizados com sucesso!'
            )
        )