from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import unicodedata
import re


def normalizar_nome(valor):
    valor = valor.strip()
    valor = " ".join(valor.split())
    valor = unicodedata.normalize("NFKD", valor)
    valor = "".join(
        caractere
        for caractere in valor
        if not unicodedata.combining(caractere)
    )
    return valor.casefold()


def normalizar_nome_empresa_base(valor):
    valor = normalizar_nome(valor)
    valor = re.sub(r"[^a-z0-9\s]", " ", valor)
    valor = " ".join(valor.split())

    sufixos = {
        "sa",
        "s",
        "a",
        "s-a",
        "ltda",
        "limitada",
        "eireli",
        "mei",
        "me",
        "epp",
        "holding",
        "inc",
        "llc",
        "corp",
        "corporation",
    }

    palavras = valor.split()

    while palavras and palavras[-1] in sufixos:
        palavras.pop()

    return " ".join(palavras)


# ============================================================
# OPÇÕES DE MODALIDADE
# ============================================================

MODALIDADE_CHOICES = [
    ("Remoto", _("Remoto")),
    ("Híbrido", _("Híbrido")),
    ("Presencial", _("Presencial")),
]


# ============================================================
# ETAPAS / STATUS DA CANDIDATURA
# ============================================================

STATUS_CHOICES = [
    ("Aplicado", _("Aplicado")),
    ("Triagem", _("Triagem")),
    ("Entrevista RH", _("Entrevista RH")),
    ("Entrevista Gestor", _("Entrevista Gestor")),
    ("Teste Técnico", _("Teste Técnico")),
    ("Finalista", _("Finalista")),
    ("Aprovado", _("Aprovado")),
    ("Recusado", _("Recusado")),
    ("Desistiu", _("Desistiu")),
]


class Empresa(models.Model):

    name = models.CharField(max_length=200)

    name_normalized = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

    def save(self, *args, **kwargs):

        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EmpresaAlias(models.Model):

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="aliases"
    )

    name = models.CharField(
        max_length=200
    )

    name_normalized = models.CharField(
        max_length=200,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} → {self.empresa.name}"


class Cargo(models.Model):

    name = models.CharField(
        max_length=200
    )

    name_normalized = models.CharField(
        max_length=200,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

    def save(self, *args, **kwargs):

        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Candidatura(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="candidaturas",
        null=True,
        blank=True
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="candidaturas"
    )

    cargo = models.CharField(
        max_length=200
    )

    local_vaga = models.CharField(
        max_length=200,
        blank=True
    )

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
        choices=MODALIDADE_CHOICES
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Aplicado"
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


class LanguageSuggestion(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="language_suggestions"
    )

    idioma = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.idioma