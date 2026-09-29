from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .perfil_usuario import PerfilUsuario

import unicodedata
import re


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalizar_nome(valor):

    valor = valor.strip()

    valor = " ".join(
        valor.split()
    )

    valor = unicodedata.normalize(
        "NFKD",
        valor
    )

    valor = "".join(
        caractere
        for caractere in valor
        if not unicodedata.combining(caractere)
    )

    return valor.casefold()


def normalizar_nome_empresa_base(valor):

    valor = normalizar_nome(
        valor
    )

    valor = re.sub(
        r"[^a-z0-9\s]",
        " ",
        valor
    )

    valor = " ".join(
        valor.split()
    )

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

    while (
        palavras
        and palavras[-1] in sufixos
    ):
        palavras.pop()

    return " ".join(
        palavras
    )


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


# ============================================================
# EMPRESA
# ============================================================

class Empresa(models.Model):

    name = models.CharField(
        max_length=200
    )

    name_normalized = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    setor = models.CharField(
        max_length=150,
        blank=True
    )

    localizacao = models.CharField(
        max_length=200,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    pagina_carreiras = models.URLField(
        blank=True
    )

    logo = models.URLField(
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

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return self.name


# ============================================================
# ALIASES DE EMPRESA
# ============================================================

class EmpresaAlias(models.Model):

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

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="aliases"
    )

    def save(self, *args, **kwargs):

        self.name = " ".join(
            self.name.strip().split()
        )

        self.name_normalized = normalizar_nome(
            self.name
        )

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return (
            f"{self.name} "
            f"({self.empresa.name})"
        )


# ============================================================
# CARGO
# ============================================================

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

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return self.name


# ============================================================
# CANDIDATURA
# ============================================================

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

        return (
            f"{self.cargo} - "
            f"{self.empresa.name}"
        )


# ============================================================
# SUGESTÃO DE IDIOMA
# ============================================================

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


# ============================================================
# SOLICITAÇÃO DE EMPRESA
# ============================================================

class SolicitacaoEmpresa(models.Model):

    STATUS_CHOICES = [
        (
            "pendente",
            "Pendente"
        ),
        (
            "aprovada",
            "Aprovada"
        ),
        (
            "rejeitada",
            "Rejeitada"
        ),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitacoes_empresa"
    )

    name = models.CharField(
        max_length=255
    )

    name_normalized = models.CharField(
        max_length=255,
        db_index=True
    )

    website = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        self.name_normalized = normalizar_nome(
            self.name
        )

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return (
            f"{self.name} "
            f"({self.get_status_display()})"
        )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Solicitação de empresa"
        )

        verbose_name_plural = (
            "Solicitações de empresas"
        )


# ============================================================
# REGISTRO DE AUDITORIA
# ============================================================

class RegistroAuditoria(models.Model):
    
    EVENTO_CHOICES = [
        ("request", "Requisição"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("login_failed", "Login recusado"),
        ("empresa_aprovada", "Empresa aprovada"),
        ("empresa_rejeitada", "Empresa rejeitada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registros_auditoria"
    )

    evento = models.CharField(
        max_length=30,
        choices=EVENTO_CHOICES,
        db_index=True
    )

    metodo = models.CharField(
        max_length=10,
        blank=True
    )

    rota = models.CharField(
        max_length=500,
        blank=True
    )

    status_http = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    referer = models.URLField(
        max_length=1000,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):

        usuario = (
            self.usuario.username
            if self.usuario
            else "Anônimo"
        )

        return (
            f"{self.evento} - "
            f"{usuario} - "
            f"{self.created_at}"
        )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Registro de auditoria"
        )

        verbose_name_plural = (
            "Registros de auditoria"
        )
    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = (
            "Registro de auditoria"
        )

        verbose_name_plural = (
            "Registros de auditoria"
        )