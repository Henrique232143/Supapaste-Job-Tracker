from django.db import models
from django.contrib.auth.models import User  # 🆕 ALTERADO


class Empresa(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Candidatura(models.Model):
    # 🆕 ALTERADO: cada candidatura agora pertence a um usuário
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='candidaturas',
        null=True,
        blank=True
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='candidaturas'
    )

    cargo = models.CharField(max_length=200)

    data_candidatura = models.DateField()

    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    link_vaga = models.URLField(
        blank=True
    )

    modalidade = models.CharField(
        max_length=20,
        choices=[
            ('Remoto', 'Remoto'),
            ('Híbrido', 'Híbrido'),
            ('Presencial', 'Presencial'),
        ]
    )

    status = models.CharField(
        max_length=30,
        choices=[
            ('Aplicado', 'Aplicado'),
            ('Triagem', 'Triagem'),
            ('Entrevista RH', 'Entrevista RH'),
            ('Entrevista Gestor', 'Entrevista Gestor'),
            ('Teste Técnico', 'Teste Técnico'),
            ('Finalista', 'Finalista'),
            ('Aprovado', 'Aprovado'),
            ('Recusado', 'Recusado'),
            ('Desistiu', 'Desistiu'),
        ],
        default='Aplicado'
    )

    observacoes = models.TextField(
        blank=True
    )

    ultimo_contato = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.cargo} - {self.empresa.name}"