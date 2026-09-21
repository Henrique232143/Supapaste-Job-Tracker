from django.urls import path
from . import views


urlpatterns = [

    # Landing Page
    path(
        '',
        views.landing,
        name='landing'
    ),

    # Empresas
    path(
        'empresas/',
        views.lista_empresas,
        name='lista_empresas'
    ),

    # Candidaturas
    path(
        'candidaturas/',
        views.candidaturas,
        name='candidaturas'
    ),

    path(
        'candidaturas/nova/',
        views.nova_candidatura,
        name='nova_candidatura'
    ),

    # Autenticação
    path(
        'cadastro/',
        views.cadastro,
        name='cadastro'
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
