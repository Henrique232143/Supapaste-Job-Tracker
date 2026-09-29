from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from .models import RegistroAuditoria


def obter_rota(
    request
):

    if request is None:
        return ""

    return request.path[:500]


def obter_metodo(
    request
):

    if request is None:
        return ""

    return getattr(
        request,
        "method",
        ""
    )[:10]


def obter_ip(
    request
):

    if request is None:
        return None

    return request.META.get(
        "REMOTE_ADDR"
    )


def obter_user_agent(
    request
):

    if request is None:
        return ""

    return (
        request.META.get(
            "HTTP_USER_AGENT",
            ""
        )[:1000]
    )


def obter_referer(
    request
):

    if request is None:
        return ""

    return (
        request.META.get(
            "HTTP_REFERER",
            ""
        )[:1000]
    )


@receiver(user_logged_in)
def registrar_login(
    sender,
    request,
    user,
    **kwargs
):

    RegistroAuditoria.objects.create(
        usuario=user,
        evento="login",
        metodo=obter_metodo(
            request
        ),
        rota=obter_rota(
            request
        ),
        status_http=200,
        ip_address=obter_ip(
            request
        ),
        user_agent=obter_user_agent(
            request
        ),
        referer=obter_referer(
            request
        ),
    )


@receiver(user_logged_out)
def registrar_logout(
    sender,
    request,
    user,
    **kwargs
):

    RegistroAuditoria.objects.create(
        usuario=user,
        evento="logout",
        metodo=obter_metodo(
            request
        ),
        rota=obter_rota(
            request
        ),
        status_http=200,
        ip_address=obter_ip(
            request
        ),
        user_agent=obter_user_agent(
            request
        ),
        referer=obter_referer(
            request
        ),
    )


@receiver(user_login_failed)
def registrar_login_falhou(
    sender,
    credentials,
    request,
    **kwargs
):

    RegistroAuditoria.objects.create(
        usuario=None,
        evento="login_failed",
        metodo=obter_metodo(
            request
        ),
        rota=obter_rota(
            request
        ),
        status_http=401,
        ip_address=obter_ip(
            request
        ),
        user_agent=obter_user_agent(
            request
        ),
        referer=obter_referer(
            request
        ),
    )