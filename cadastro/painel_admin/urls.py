from django.urls import path

from . import views


app_name = "painel_admin"


urlpatterns = [

    path(
        "auditoria/",
        views.auditoria,
        name="auditoria"
    ),

    path(
        "auditoria/<int:registro_id>/",
        views.auditoria_detalhe,
        name="auditoria_detalhe"
    ),

]