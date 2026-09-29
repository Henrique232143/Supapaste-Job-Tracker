from .models import RegistroAuditoria


class AuditoriaMiddleware:

    ROTAS_IGNORADAS = (
        "/static/",
        "/media/",
        "/favicon.ico",
        "/admin/jsi18n/",
        "/painel-admin/auditoria/",
    )

    ROTAS_AUTENTICACAO = (
        "/login/",
        "/logout/",
    )

    def __init__(
        self,
        get_response
    ):
        self.get_response = get_response


    def __call__(
        self,
        request
    ):

        response = self.get_response(
            request
        )

        if self.deve_registrar(
            request
        ):
            self.registrar(
                request,
                response
            )

        return response


    def deve_registrar(
        self,
        request
    ):

        rota = request.path

        # =====================================================
        # ROTAS IGNORADAS
        # =====================================================

        if any(
            rota.startswith(prefixo)
            for prefixo
            in self.ROTAS_IGNORADAS
        ):
            return False


        # =====================================================
        # AUTENTICAÇÃO
        #
        # Login e logout possuem eventos próprios
        # registrados através dos signals.
        # =====================================================

        if rota in self.ROTAS_AUTENTICACAO:
            return False

        return True


    def obter_ip(
        self,
        request
    ):

        ip = request.META.get(
            "REMOTE_ADDR"
        )

        if not ip:
            return None

        return ip


    def obter_user_agent(
        self,
        request
    ):

        return (
            request.META.get(
                "HTTP_USER_AGENT",
                ""
            )[:1000]
        )


    def obter_referer(
        self,
        request
    ):

        return (
            request.META.get(
                "HTTP_REFERER",
                ""
            )[:1000]
        )


    def registrar(
        self,
        request,
        response
    ):

        usuario = None

        if (
            hasattr(
                request,
                "user"
            )
            and
            request.user.is_authenticated
        ):
            usuario = request.user

        try:

            RegistroAuditoria.objects.create(
                usuario=usuario,
                evento="request",
                metodo=request.method[:10],
                rota=request.path[:500],
                status_http=(
                    response.status_code
                ),
                ip_address=(
                    self.obter_ip(
                        request
                    )
                ),
                user_agent=(
                    self.obter_user_agent(
                        request
                    )
                ),
                referer=(
                    self.obter_referer(
                        request
                    )
                ),
            )

        except Exception:

            # Uma falha na auditoria
            # não deve impedir o funcionamento
            # da aplicação principal.
            pass