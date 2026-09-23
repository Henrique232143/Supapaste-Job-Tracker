from collections import Counter

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.urls import reverse

from django.db.models import (
    Avg,
    Max,
    Min
)

from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from .models import (
    Empresa,
    EmpresaAlias,
    Cargo,
    Candidatura,
    normalizar_nome
)

from .forms import (
    CandidaturaForm,
    CadastroForm,
    EmpresaForm,
    CargoForm,
    StatusCandidaturaForm,
    LanguageSuggestionForm
)

from .servicos import encontrar_empresas_semelhantes


def landing(request):

    return render(
        request,
        'cadastro/landing.html'
    )


@login_required(login_url='login')
def lista_empresas(request):

    empresas = Empresa.objects.all()

    return render(
        request,
        'cadastro/lista_empresas.html',
        {
            'empresas': empresas
        }
    )


@login_required(login_url='login')
def candidaturas(request):

    candidaturas_queryset = (
        Candidatura.objects
        .filter(
            usuario=request.user
        )
        .select_related('empresa')
        .order_by('-data_candidatura')
    )

    total = candidaturas_queryset.count()


    # =========================================================
    # CONTADORES PRINCIPAIS
    # =========================================================

    status_lista = list(
        candidaturas_queryset.values_list(
            'status',
            flat=True
        )
    )

    status_contagem = Counter(
        status_lista
    )


    em_andamento_status = [
        'Aplicado',
        'Triagem',
        'Entrevista RH',
        'Entrevista Gestor',
        'Teste Técnico',
        'Finalista',
    ]

    em_andamento = sum(
        status_contagem.get(
            status,
            0
        )
        for status in em_andamento_status
    )


    entrevistas = (
        status_contagem.get(
            'Entrevista RH',
            0
        )
        +
        status_contagem.get(
            'Entrevista Gestor',
            0
        )
    )


    finalistas = status_contagem.get(
        'Finalista',
        0
    )


    aprovadas = status_contagem.get(
        'Aprovado',
        0
    )


    recusadas = status_contagem.get(
        'Recusado',
        0
    )


    # =========================================================
    # FUNÇÃO AUXILIAR PARA DISTRIBUIÇÕES
    # =========================================================

    def montar_distribuicao(
        contador,
        limite=None
    ):

        itens = contador.most_common(
            limite
        )

        resultado = []

        for nome, quantidade in itens:

            percentual = 0

            if total > 0:

                percentual = round(
                    quantidade / total * 100
                )

            resultado.append({
                'label': nome,
                'total': quantidade,
                'percentual': percentual,
            })

        return resultado


    # =========================================================
    # STATUS
    # =========================================================

    ordem_status = [
        'Aplicado',
        'Triagem',
        'Entrevista RH',
        'Entrevista Gestor',
        'Teste Técnico',
        'Finalista',
        'Aprovado',
        'Recusado',
        'Desistiu',
    ]


    status_distribuicao = []

    for status in ordem_status:

        quantidade = status_contagem.get(
            status,
            0
        )

        if quantidade == 0:
            continue

        percentual = 0

        if total > 0:

            percentual = round(
                quantidade / total * 100
            )

        status_distribuicao.append({
            'label': status,
            'total': quantidade,
            'percentual': percentual,
        })


    # =========================================================
    # MODALIDADE
    # =========================================================

    modalidade_lista = list(
        candidaturas_queryset.values_list(
            'modalidade',
            flat=True
        )
    )

    modalidade_contagem = Counter(
        modalidade_lista
    )

    modalidade_distribuicao = montar_distribuicao(
        modalidade_contagem
    )


    # =========================================================
    # CARGOS
    # =========================================================

    cargo_lista = list(
        candidaturas_queryset.values_list(
            'cargo',
            flat=True
        )
    )

    cargo_contagem = Counter(
        cargo_lista
    )

    cargo_distribuicao = montar_distribuicao(
        cargo_contagem,
        limite=5
    )


    # =========================================================
    # EMPRESAS
    # =========================================================

    empresa_lista = list(
        candidaturas_queryset.values_list(
            'empresa__name',
            flat=True
        )
    )

    empresa_contagem = Counter(
        empresa_lista
    )

    empresa_distribuicao = montar_distribuicao(
        empresa_contagem,
        limite=5
    )


    # =========================================================
    # LOCAL DA VAGA
    # =========================================================

    local_lista = []

    for candidatura in candidaturas_queryset:

        local = (
            candidatura.local_vaga
            or ''
        ).strip()

        if not local:

            local = 'Não informado'

        local_lista.append(
            local
        )


    local_contagem = Counter(
        local_lista
    )

    local_distribuicao = montar_distribuicao(
        local_contagem,
        limite=5
    )


    # =========================================================
    # SALÁRIOS
    # =========================================================

    salarios = candidaturas_queryset.aggregate(
        media=Avg('salario'),
        maior=Max('salario'),
        menor=Min('salario'),
    )


    salario_medio = salarios['media']
    salario_maior = salarios['maior']
    salario_menor = salarios['menor']


    # =========================================================
    # CARGO PRINCIPAL
    # =========================================================

    cargo_principal = None

    if cargo_contagem:

        nome_cargo, quantidade = (
            cargo_contagem.most_common(1)[0]
        )

        percentual = 0

        if total > 0:

            percentual = round(
                quantidade / total * 100
            )

        cargo_principal = {
            'nome': nome_cargo,
            'quantidade': quantidade,
            'percentual': percentual,
        }


    # =========================================================
    # CANDIDATURAS RECENTES
    # =========================================================

    recentes = candidaturas_queryset[:8]


    return render(
        request,
        'cadastro/candidaturas.html',
        {
            'candidaturas': candidaturas_queryset,

            'recentes': recentes,

            'total': total,

            'em_andamento': em_andamento,

            'entrevistas': entrevistas,

            'finalistas': finalistas,

            'aprovadas': aprovadas,

            'recusadas': recusadas,

            'status_distribuicao': status_distribuicao,

            'modalidade_distribuicao': modalidade_distribuicao,

            'cargo_distribuicao': cargo_distribuicao,

            'empresa_distribuicao': empresa_distribuicao,

            'local_distribuicao': local_distribuicao,

            'cargo_principal': cargo_principal,

            'salario_medio': salario_medio,

            'salario_maior': salario_maior,

            'salario_menor': salario_menor,
        }
    )


@login_required(login_url='login')
def detalhe_candidatura(
    request,
    candidatura_id
):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'empresa'
        ),
        id=candidatura_id,
        usuario=request.user
    )


    etapas = [
        'Aplicado',
        'Triagem',
        'Entrevista RH',
        'Entrevista Gestor',
        'Teste Técnico',
        'Finalista',
        'Aprovado',
    ]


    etapa_atual = -1


    if candidatura.status in etapas:

        etapa_atual = etapas.index(
            candidatura.status
        )


    status_encerrado = candidatura.status in [
        'Recusado',
        'Desistiu',
    ]


    status_form = StatusCandidaturaForm(
        instance=candidatura
    )


    return render(
        request,
        'cadastro/detalhe_candidatura.html',
        {
            'candidatura': candidatura,

            'etapas': etapas,

            'etapa_atual': etapa_atual,

            'status_encerrado': status_encerrado,

            'status_form': status_form,
        }
    )


@login_required(login_url='login')
def atualizar_status_candidatura(
    request,
    candidatura_id
):

    candidatura = get_object_or_404(
        Candidatura,
        id=candidatura_id,
        usuario=request.user
    )


    if request.method != 'POST':

        return redirect(
            'detalhe_candidatura',
            candidatura_id=candidatura.id
        )


    form = StatusCandidaturaForm(
        request.POST,
        instance=candidatura
    )


    if form.is_valid():

        form.save()


    return redirect(
        'detalhe_candidatura',
        candidatura_id=candidatura.id
    )


# =============================================================
# EDITAR CANDIDATURA
# =============================================================

@login_required(login_url='login')
def editar_candidatura(
    request,
    candidatura_id
):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'empresa'
        ),
        id=candidatura_id,
        usuario=request.user
    )


    if request.method == 'POST':

        form = CandidaturaForm(
            request.POST,
            instance=candidatura
        )


        if form.is_valid():

            form.save()

            return redirect(
                'detalhe_candidatura',
                candidatura_id=candidatura.id
            )

    else:

        form = CandidaturaForm(
            instance=candidatura
        )


    return render(
        request,
        'cadastro/editar_candidatura.html',
        {
            'form': form,

            'candidatura': candidatura,
        }
    )


# =============================================================
# EXCLUIR CANDIDATURA
# =============================================================

@login_required(login_url='login')
def excluir_candidatura(
    request,
    candidatura_id
):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'empresa'
        ),
        id=candidatura_id,
        usuario=request.user
    )


    if request.method == 'POST':

        candidatura.delete()

        return redirect(
            'candidaturas'
        )


    return render(
        request,
        'cadastro/excluir_candidatura.html',
        {
            'candidatura': candidatura,
        }
    )


@login_required(login_url='login')
def nova_candidatura(request):

    empresa_id = request.GET.get(
        'empresa'
    )

    cargo_id = request.GET.get(
        'cargo'
    )


    if request.method == 'POST':

        form = CandidaturaForm(
            request.POST
        )

        if form.is_valid():

            candidatura = form.save(
                commit=False
            )

            candidatura.usuario = request.user

            candidatura.save()

            return redirect(
                'candidaturas'
            )

    else:

        initial = {}

        if empresa_id:

            initial['empresa'] = empresa_id

        if cargo_id:

            initial['cargo_catalogo'] = cargo_id

        form = CandidaturaForm(
            initial=initial
        )


    return render(
        request,
        'cadastro/nova_candidatura.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def nova_empresa(request):

    semelhantes = []


    if request.method == 'POST':

        form = EmpresaForm(
            request.POST
        )


        if form.is_valid():

            nome = form.cleaned_data[
                'name'
            ]


            semelhantes = (
                encontrar_empresas_semelhantes(
                    nome
                )
            )


            confirmar = (
                request.POST.get(
                    'confirmar_cadastro'
                )
                == '1'
            )


            if semelhantes and not confirmar:

                return render(
                    request,
                    'cadastro/nova_empresa.html',
                    {
                        'form': form,
                        'semelhantes': semelhantes,
                    }
                )


            empresa = form.save()


            return redirect(
                f"{reverse('nova_candidatura')}"
                f"?empresa={empresa.id}"
            )


    else:

        form = EmpresaForm()


    return render(
        request,
        'cadastro/nova_empresa.html',
        {
            'form': form,
            'semelhantes': semelhantes,
        }
    )


@login_required(login_url='login')
def usar_empresa_existente(
    request,
    empresa_id
):

    empresa = get_object_or_404(
        Empresa,
        id=empresa_id
    )


    if request.method != 'POST':

        return redirect(
            'nova_candidatura'
        )


    nome_alias = request.POST.get(
        'alias',
        ''
    ).strip()


    if nome_alias:

        nome_normalizado = normalizar_nome(
            nome_alias
        )


        alias_existe = (
            EmpresaAlias.objects.filter(
                name_normalized=nome_normalizado
            ).exists()
        )


        empresa_existe = (
            Empresa.objects.filter(
                name_normalized=nome_normalizado
            ).exists()
        )


        if (
            not alias_existe
            and not empresa_existe
            and nome_normalizado
            != empresa.name_normalized
        ):

            EmpresaAlias.objects.create(
                empresa=empresa,
                name=nome_alias
            )


    return redirect(
        f"{reverse('nova_candidatura')}"
        f"?empresa={empresa.id}"
    )


@login_required(login_url='login')
def nova_cargo(request):

    if request.method == 'POST':

        form = CargoForm(
            request.POST
        )


        if form.is_valid():

            cargo = form.save()


            return redirect(
                f"{reverse('nova_candidatura')}"
                f"?cargo={cargo.id}"
            )


    else:

        form = CargoForm()


    return render(
        request,
        'cadastro/novo_cargo.html',
        {
            'form': form
        }
    )


def cadastro(request):

    if request.method == 'POST':

        form = CadastroForm(
            request.POST
        )


        if form.is_valid():

            nome = form.cleaned_data[
                'first_name'
            ]

            email = form.cleaned_data[
                'email'
            ]

            senha = form.cleaned_data[
                'senha'
            ]


            usuario = User.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome
            )


            login(
                request,
                usuario
            )


            return redirect(
                'candidaturas'
            )


    else:

        form = CadastroForm()


    return render(
        request,
        'cadastro/cadastro.html',
        {
            'form': form
        }
    )


def login_usuario(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email'
        )

        senha = request.POST.get(
            'senha'
        )


        usuario = authenticate(
            request,
            username=email,
            password=senha
        )


        if usuario is not None:

            login(
                request,
                usuario
            )


            return redirect(
                'candidaturas'
            )


        return render(
            request,
            'cadastro/login.html',
            {
                'erro':
                    'E-mail ou senha incorretos.'
            }
        )


    return render(
        request,
        'cadastro/login.html'
    )


@login_required(login_url='login')
def logout_usuario(request):

    logout(request)

    return redirect(
        'login'
    )


from django.utils.http import url_has_allowed_host_and_scheme


def sugerir_idioma(request):

    if request.method == 'POST':

        form = LanguageSuggestionForm(
            request.POST
        )


        if form.is_valid():

            sugestao = form.save(
                commit=False
            )


            if request.user.is_authenticated:

                sugestao.usuario = request.user


            sugestao.save()


    proxima_url = request.POST.get(
        'next'
    )


    if not proxima_url:

        if request.user.is_authenticated:

            return redirect(
                'candidaturas'
            )

        return redirect(
            'landing'
        )


    if not url_has_allowed_host_and_scheme(
        proxima_url,
        allowed_hosts={
            request.get_host()
        },
        require_https=request.is_secure()
    ):

        if request.user.is_authenticated:

            return redirect(
                'candidaturas'
            )

        return redirect(
            'landing'
        )


    return redirect(
        proxima_url
    )