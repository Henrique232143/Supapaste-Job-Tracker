from datetime import datetime, time, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from cadastro.models import RegistroAuditoria


User = get_user_model()


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

    usuario_id = (
        request.GET.get("usuario", "")
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

    status_faixa = (
        request.GET.get("status_faixa", "")
        .strip()
    )

    periodo = (
        request.GET.get("periodo", "")
        .strip()
    )

    data_inicio = (
        request.GET.get("data_inicio", "")
        .strip()
    )

    data_fim = (
        request.GET.get("data_fim", "")
        .strip()
    )

    ordenacao = (
        request.GET.get("ordenacao", "recentes")
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
    # USUÁRIO
    # =========================================================

    if usuario_id.isdigit():

        registros = registros.filter(
            usuario_id=int(usuario_id)
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
    # STATUS HTTP EXATO
    # =========================================================

    if status_http.isdigit():

        registros = registros.filter(
            status_http=int(status_http)
        )


    # =========================================================
    # FAIXA DE STATUS HTTP
    # =========================================================

    if status_faixa == "2xx":

        registros = registros.filter(
            status_http__gte=200,
            status_http__lt=300
        )

    elif status_faixa == "3xx":

        registros = registros.filter(
            status_http__gte=300,
            status_http__lt=400
        )

    elif status_faixa == "4xx":

        registros = registros.filter(
            status_http__gte=400,
            status_http__lt=500
        )

    elif status_faixa == "5xx":

        registros = registros.filter(
            status_http__gte=500,
            status_http__lt=600
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
    # DATA INICIAL
    # =========================================================

    if data_inicio:

        try:

            data_inicio_obj = datetime.strptime(
                data_inicio,
                "%Y-%m-%d"
            ).date()

            inicio_dia = timezone.make_aware(
                datetime.combine(
                    data_inicio_obj,
                    time.min
                )
            )

            registros = registros.filter(
                created_at__gte=inicio_dia
            )

        except ValueError:
            pass


    # =========================================================
    # DATA FINAL
    # =========================================================

    if data_fim:

        try:

            data_fim_obj = datetime.strptime(
                data_fim,
                "%Y-%m-%d"
            ).date()

            fim_dia = timezone.make_aware(
                datetime.combine(
                    data_fim_obj,
                    time.max
                )
            )

            registros = registros.filter(
                created_at__lte=fim_dia
            )

        except ValueError:
            pass


    # =========================================================
    # ORDENAÇÃO
    # =========================================================

    if ordenacao == "antigos":

        registros = registros.order_by(
            "created_at"
        )

    elif ordenacao == "status":

        registros = registros.order_by(
            "status_http",
            "-created_at"
        )

    elif ordenacao == "usuario":

        registros = registros.order_by(
            "usuario__username",
            "-created_at"
        )

    elif ordenacao == "evento":

        registros = registros.order_by(
            "evento",
            "-created_at"
        )

    else:

        registros = registros.order_by(
            "-created_at"
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
    # USUÁRIOS DISPONÍVEIS NO FILTRO
    # =========================================================

    usuarios = (
        User.objects
        .filter(
            registros_auditoria__isnull=False
        )
        .distinct()
        .order_by("username")
    )


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
            "usuario_selecionado": usuario_id,
            "evento_selecionado": evento,
            "metodo_selecionado": metodo,
            "status_selecionado": status_http,
            "status_faixa_selecionado": status_faixa,
            "periodo_selecionado": periodo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "ordenacao_selecionada": ordenacao,

            "usuarios": usuarios,

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

            "status_faixas": [
                ("2xx", "2xx — Sucesso"),
                ("3xx", "3xx — Redirecionamento"),
                ("4xx", "4xx — Erro do cliente"),
                ("5xx", "5xx — Erro do servidor"),
            ],

            "ordenacoes": [
                ("recentes", "Mais recentes"),
                ("antigos", "Mais antigos"),
                ("status", "Status HTTP"),
                ("usuario", "Usuário"),
                ("evento", "Evento"),
            ],
        }
    )


@staff_member_required(
    login_url="/admin/login/"
)
def auditoria_detalhe(
    request,
    registro_id
):

    registro = get_object_or_404(
        RegistroAuditoria.objects.select_related(
            "usuario"
        ),
        id=registro_id
    )

    contexto = {
        "registro": registro,
    }

    return render(
        request,
        "painel_admin/auditoria_detalhe.html",
        contexto
    )