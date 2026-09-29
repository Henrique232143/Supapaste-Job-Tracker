from django.urls import resolve

from .models import RegistroAuditoria


class AuditoriaMiddleware:

    ROTAS_IGNORADAS = (
        "/static/",
        "/media/",
        "/favicon.ico",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if self.deve_registrar(request):
            self.registrar(request, response)

        return response

    def deve_registrar(self, request):

        rota = request.path

        if any(
            rota.startswith(prefixo)
            for prefixo in self.ROTAS_IGNORADAS
        ):
            return False

        # Login/logout já são registrados pelos signals.
        if rota in (
            "/login/",
            "/logout/",
        ):
            return False

        return True

    def registrar(
        self,
        request,
        response
    ):

        usuario = None

        if (
            hasattr(request, "user")
            and request.user.is_authenticated
        ):
            usuario = request.user

        try:

            RegistroAuditoria.objects.create(
                usuario=usuario,
                evento="request",
                metodo=request.method[:10],
                rota=request.path[:500],
                status_http=response.status_code,
            )

        except Exception:
            # Auditoria nunca deve derrubar
            # a aplicação principal.
            pass