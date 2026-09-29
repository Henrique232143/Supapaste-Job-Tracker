from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)

from django.dispatch import receiver

from .models import RegistroAuditoria


def obter_rota(request):

    if request is None:
        return ""

    return request.path[:500]


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):

    RegistroAuditoria.objects.create(
        usuario=user,
        evento="login",
        metodo=getattr(request, "method", ""),
        rota=obter_rota(request),
        status_http=200,
    )


@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):

    RegistroAuditoria.objects.create(
        usuario=user,
        evento="logout",
        metodo=getattr(request, "method", ""),
        rota=obter_rota(request),
        status_http=200,
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
        metodo=getattr(request, "method", ""),
        rota=obter_rota(request),
        status_http=401,
    )