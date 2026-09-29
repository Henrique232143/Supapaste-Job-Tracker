from django.contrib import admin
from django.db import transaction
from django.utils import timezone

from .models import (
    Empresa,
    Candidatura,
    SolicitacaoEmpresa,
    RegistroAuditoria,
    normalizar_nome,
)


# =============================================================
# IDENTIDADE DO ADMIN
# =============================================================

admin.site.site_header = "Job Tracker"

admin.site.site_title = "Job Tracker Admin"

admin.site.index_title = "Administração do Job Tracker"


# =============================================================
# EMPRESAS
# =============================================================

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "website",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# =============================================================
# CANDIDATURAS
# =============================================================

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "empresa",
        "cargo",
        "status",
        "data_candidatura",
    )

    list_filter = (
        "status",
        "modalidade",
    )

    search_fields = (
        "usuario__username",
        "empresa__name",
        "cargo",
    )

    ordering = (
        "-data_candidatura",
    )


# =============================================================
# SOLICITAÇÕES DE EMPRESAS
# =============================================================

@admin.register(SolicitacaoEmpresa)
class SolicitacaoEmpresaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "usuario",
        "status",
        "website",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "usuario__username",
        "usuario__email",
    )

    readonly_fields = (
        "usuario",
        "name",
        "name_normalized",
        "website",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    actions = (
        "aprovar_solicitacoes",
        "rejeitar_solicitacoes",
    )

    # =========================================================
    # APROVAR
    # =========================================================

    @admin.action(
        description="Aprovar solicitações selecionadas"
    )
    def aprovar_solicitacoes(
        self,
        request,
        queryset
    ):

        aprovadas = 0

        empresas_criadas = 0

        empresas_existentes = 0

        solicitacoes = queryset.filter(
            status="pendente"
        )

        for solicitacao in solicitacoes:

            with transaction.atomic():

                nome_normalizado = normalizar_nome(
                    solicitacao.name
                )

                empresa_existente = (
                    Empresa.objects
                    .filter(
                        name_normalized=nome_normalizado
                    )
                    .first()
                )

                if empresa_existente:

                    empresas_existentes += 1

                else:

                    Empresa.objects.create(
                        name=solicitacao.name,
                        website=solicitacao.website,
                    )

                    empresas_criadas += 1

                solicitacao.status = "aprovada"

                solicitacao.save(
                    update_fields=[
                        "status",
                        "updated_at",
                    ]
                )

                aprovadas += 1

        self.message_user(
            request,
            (
                f"{aprovadas} solicitação(ões) aprovada(s). "
                f"{empresas_criadas} empresa(s) criada(s). "
                f"{empresas_existentes} empresa(s) já existia(m)."
            )
        )

    # =========================================================
    # REJEITAR
    # =========================================================

    @admin.action(
        description="Rejeitar solicitações selecionadas"
    )
    def rejeitar_solicitacoes(
        self,
        request,
        queryset
    ):

        quantidade = queryset.filter(
            status="pendente"
        ).update(
            status="rejeitada"
        )

        self.message_user(
            request,
            (
                f"{quantidade} solicitação(ões) "
                f"rejeitada(s)."
            )
        )


# =============================================================
# AUDITORIA / ATIVIDADE E SEGURANÇA
# =============================================================

@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):

    list_display = (
        "horario_local",
        "usuario_exibicao",
        "evento",
        "metodo",
        "rota",
        "status_http",
    )

    list_filter = (
        "evento",
        "metodo",
        "status_http",
        "created_at",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "rota",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 50

    readonly_fields = (
        "usuario",
        "evento",
        "metodo",
        "rota",
        "status_http",
        "created_at",
    )

    # =========================================================
    # HORÁRIO LOCAL
    # =========================================================

    @admin.display(
        description="Data e hora",
        ordering="created_at"
    )
    def horario_local(self, obj):

        data = timezone.localtime(
            obj.created_at
        )

        return data.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    # =========================================================
    # USUÁRIO
    # =========================================================

    @admin.display(
        description="Usuário"
    )
    def usuario_exibicao(self, obj):

        if obj.usuario:

            return obj.usuario.username

        return "Anônimo"

    # =========================================================
    # AUDITORIA É SOMENTE LEITURA
    # =========================================================

    def has_add_permission(
        self,
        request
    ):

        return False

    def has_change_permission(
        self,
        request,
        obj=None
    ):

        return False

    def has_delete_permission(
        self,
        request,
        obj=None
    ):

        return False

    def has_view_permission(
        self,
        request,
        obj=None
    ):

        return (
            request.user.is_active
            and request.user.is_staff
        )