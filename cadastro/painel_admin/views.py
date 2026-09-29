from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from cadastro.models import RegistroAuditoria


@staff_member_required(
    login_url="/admin/login/"
)
def auditoria(request):

    registros = (
        RegistroAuditoria.objects
        .select_related("usuario")
        .all()
    )

    # =========================================================
    # FILTROS
    # =========================================================

    busca = (
        request.GET.get("busca", "")
        .strip()
    )

    evento = (
        request.GET.get("evento", "")
        .strip()
    )

    metodo = (
        request.GET.get("metodo", "")
        .strip()
    )

    status_http = (
        request.GET.get("status", "")
        .strip()
    )

    periodo = (
        request.GET.get("periodo", "")
        .strip()
    )


    # =========================================================
    # BUSCA
    # =========================================================

    if busca:

        registros = registros.filter(
            Q(
                usuario__username__icontains=busca
            )
            |
            Q(
                usuario__email__icontains=busca
            )
            |
            Q(
                rota__icontains=busca
            )
        )


    # =========================================================
    # EVENTO
    # =========================================================

    if evento:

        registros = registros.filter(
            evento=evento
        )


    # =========================================================
    # MÉTODO
    # =========================================================

    if metodo:

        registros = registros.filter(
            metodo=metodo
        )


    # =========================================================
    # STATUS HTTP
    # =========================================================

    if status_http.isdigit():

        registros = registros.filter(
            status_http=int(status_http)
        )


    # =========================================================
    # PERÍODO
    # =========================================================

    agora = timezone.now()

    if periodo == "hoje":

        inicio = agora.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        registros = registros.filter(
            created_at__gte=inicio
        )

    elif periodo == "7dias":

        registros = registros.filter(
            created_at__gte=(
                agora - timedelta(days=7)
            )
        )

    elif periodo == "30dias":

        registros = registros.filter(
            created_at__gte=(
                agora - timedelta(days=30)
            )
        )


    # =========================================================
    # MÉTRICAS
    # =========================================================

    inicio_hoje = agora.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    registros_hoje = (
        RegistroAuditoria.objects
        .filter(
            created_at__gte=inicio_hoje
        )
    )

    metricas = {
        "requisicoes": (
            registros_hoje
            .filter(evento="request")
            .count()
        ),

        "logins": (
            registros_hoje
            .filter(evento="login")
            .count()
        ),

        "falhas_login": (
            registros_hoje
            .filter(evento="login_failed")
            .count()
        ),

        "usuarios": (
            registros_hoje
            .exclude(usuario=None)
            .values("usuario")
            .distinct()
            .count()
        ),
    }


    # =========================================================
    # PAGINAÇÃO
    # =========================================================

    paginator = Paginator(
        registros,
        30
    )

    pagina = paginator.get_page(
        request.GET.get("page")
    )


    # =========================================================
    # TEMPLATE
    # =========================================================

    return render(
        request,
        "painel_admin/auditoria.html",
        {
            "pagina": pagina,
            "metricas": metricas,

            "busca": busca,
            "evento_selecionado": evento,
            "metodo_selecionado": metodo,
            "status_selecionado": status_http,
            "periodo_selecionado": periodo,

            "eventos": (
                RegistroAuditoria.EVENTO_CHOICES
            ),

            "metodos": [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            ],

            "status_http": [
                200,
                201,
                204,
                301,
                302,
                400,
                401,
                403,
                404,
                500,
            ],
        }
    )