from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.landing,
        name='landing'
    ),

    path(
        'empresas/',
        views.lista_empresas,
        name='lista_empresas'
    ),

    path(
        'empresas/nova/',
        views.nova_empresa,
        name='nova_empresa'
    ),

    path(
        'empresas/<int:empresa_id>/usar/',
        views.usar_empresa_existente,
        name='usar_empresa_existente'
    ),

    path(
        'cargos/nova/',
        views.nova_cargo,
        name='novo_cargo'
    ),

    path(
        'candidaturas/',
        views.candidaturas,
        name='candidaturas'
    ),

    path(
        'candidaturas/<int:candidatura_id>/status/',
        views.atualizar_status_candidatura,
        name='atualizar_status_candidatura'
    ),

    path(
        'candidaturas/<int:candidatura_id>/',
        views.detalhe_candidatura,
        name='detalhe_candidatura'
    ),

    path(
        'candidaturas/nova/',
        views.nova_candidatura,
        name='nova_candidatura'
    ),

    path(
        'cadastro/',
        views.cadastro,
        name='cadastro'
    ),

    path(
        'idiomas/sugerir/',
        views.sugerir_idioma,
        name='sugerir_idioma'
    ),

    path(
        'login/',
        views.login_usuario,
        name='login'
    ),

    path(
        'logout/',
        views.logout_usuario,
        name='logout'
    ),
]