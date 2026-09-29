from django import template

from cadastro.models import (
    Empresa,
    Candidatura,
    SolicitacaoEmpresa,
)


register = template.Library()


@register.simple_tag
def total_empresas():
    return Empresa.objects.count()


@register.simple_tag
def total_candidaturas():
    return Candidatura.objects.count()


@register.simple_tag
def total_solicitacoes():
    return SolicitacaoEmpresa.objects.count()


@register.simple_tag
def total_solicitacoes_pendentes():
    return SolicitacaoEmpresa.objects.filter(
        status="pendente"
    ).count()


@register.simple_tag
def solicitacoes_pendentes(limite=5):

    return (
        SolicitacaoEmpresa.objects
        .filter(status="pendente")
        .select_related("usuario")
        .order_by("-created_at")[:limite]
    )