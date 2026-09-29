from collections import Counter

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db import (
    IntegrityError,
    models,
    transaction
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

from django.utils.http import (
    url_has_allowed_host_and_scheme
)

from django.utils.translation import gettext as _

from .models import (
    Empresa,
    EmpresaAlias,
    Candidatura,
    SolicitacaoEmpresa,
    normalizar_nome
)

from .perfil_usuario import PerfilUsuario

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
        'cadastro/empresas/lista.html',
        {
            'empresas': empresas
        }
    )


# =============================================================
# DETALHE DA EMPRESA
# =============================================================

@login_required(login_url='login')
def detalhe_empresa(
    request,
    empresa_id
):

    empresa = get_object_or_404(
        Empresa,
        id=empresa_id
    )

    candidaturas_empresa = (
        Candidatura.objects
        .filter(
            empresa=empresa,
            usuario=request.user
        )
        .order_by('-data_candidatura')
    )

    total = candidaturas_empresa.count()

    status_lista = list(
        candidaturas_empresa.values_list(
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

    aprovadas = status_contagem.get(
        'Aprovado',
        0
    )

    recusadas = status_contagem.get(
        'Recusado',
        0
    )

    salarios = candidaturas_empresa.aggregate(
        media=Avg('salario'),
        maior=Max('salario'),
        menor=Min('salario'),
    )

    cargos = (
        candidaturas_empresa
        .values('cargo')
        .annotate(
            total_candidaturas=models.Count('id')
        )
        .order_by('-total_candidaturas')
    )

    return render(
        request,
        'cadastro/empresas/detalhe.html',
        {
            'empresa': empresa,
            'candidaturas_empresa': candidaturas_empresa,
            'total': total,
            'em_andamento': em_andamento,
            'entrevistas': entrevistas,
            'aprovadas': aprovadas,
            'recusadas': recusadas,
            'salario_medio': salarios['media'],
            'salario_maior': salarios['maior'],
            'salario_menor': salarios['menor'],
            'cargos': cargos,
        }
    )


@login_required(login_url='login')
def candidaturas(request):

    candidatura_criada_com_sucesso = request.session.pop(
        'candidatura_criada_com_sucesso',
        False
    )

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

    empresa_contagem = Counter(
        candidaturas_queryset.values_list(
            'empresa_id',
            flat=True
        )
    )

    empresas_por_id = Empresa.objects.in_bulk(
        empresa_contagem.keys()
    )

    empresa_distribuicao = []

    for empresa_id, quantidade in empresa_contagem.most_common(5):

        empresa = empresas_por_id.get(
            empresa_id
        )

        if empresa is None:
            continue

        percentual = 0

        if total > 0:

            percentual = round(
                quantidade / total * 100
            )

        empresa_distribuicao.append({
            'empresa_id': empresa.id,
            'label': empresa.name,
            'total': quantidade,
            'percentual': percentual,
        })

    # =========================================================
    # LOCAL DA VAGA
    # =========================================================

    local_lista = []
    locais_por_chave = {}

    for candidatura in candidaturas_queryset:

        local = (
            candidatura.local_vaga
            or ''
        ).strip()

        if not local:
            local = 'Não informado'

        chave_local = normalizar_nome(
            local
        )

        locais_por_chave.setdefault(
            chave_local,
            local
        )

        local_lista.append(
            chave_local
        )

    local_contagem = Counter(
        local_lista
    )

    local_distribuicao = montar_distribuicao(
        local_contagem,
        limite=5
    )

    for item in local_distribuicao:

        item['label'] = locais_por_chave[
            item['label']
        ]

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
        'cadastro/candidaturas/lista.html',
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
            'modalidade_distribuicao':
                modalidade_distribuicao,
            'cargo_distribuicao':
                cargo_distribuicao,
            'empresa_distribuicao':
                empresa_distribuicao,
            'local_distribuicao':
                local_distribuicao,
            'cargo_principal':
                cargo_principal,
            'salario_medio':
                salario_medio,
            'salario_maior':
                salario_maior,
            'salario_menor':
                salario_menor,
            'candidatura_criada_com_sucesso':
                candidatura_criada_com_sucesso,
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
        'cadastro/candidaturas/detalhe.html',
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
        'cadastro/candidaturas/editar.html',
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
        'cadastro/candidaturas/excluir.html',
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

            request.session[
                'candidatura_criada_com_sucesso'
            ] = True

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
        'cadastro/candidaturas/nova.html',
        {
            'form': form
        }
    )


# =============================================================
# SOLICITAR NOVA EMPRESA
# SEGURANÇA 5.6
# =============================================================

@login_required(login_url='login')
def nova_empresa(request):

    semelhantes = []

    empresa_solicitada = request.session.pop(
        'empresa_solicitada_com_sucesso',
        None
    )

    if request.method == 'POST':

        form = EmpresaForm(
            request.POST
        )

        if form.is_valid():

            nome = form.cleaned_data[
                'name'
            ]

            website = form.cleaned_data.get(
                'website',
                ''
            )

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

            # -------------------------------------------------
            # Antes de criar a solicitação, mostramos possíveis
            # empresas já existentes no catálogo.
            # -------------------------------------------------

            if semelhantes and not confirmar:

                return render(
                    request,
                    'cadastro/empresas/nova.html',
                    {
                        'form': form,
                        'semelhantes': semelhantes,
                        'empresa_solicitada':
                            empresa_solicitada,
                    }
                )

            nome_normalizado = normalizar_nome(
                nome
            )

            # -------------------------------------------------
            # Impede que o mesmo usuário crie várias solicitações
            # pendentes da mesma empresa.
            # -------------------------------------------------

            solicitacao_existente = (
                SolicitacaoEmpresa.objects
                .filter(
                    usuario=request.user,
                    name_normalized=nome_normalizado,
                    status='pendente'
                )
                .first()
            )

            if solicitacao_existente:

                request.session[
                    'empresa_solicitada_com_sucesso'
                ] = nome

                return redirect(
                    'nova_empresa'
                )

            # -------------------------------------------------
            # IMPORTANTE:
            #
            # Aqui criamos somente uma SOLICITAÇÃO.
            # Não criamos um registro de Empresa.
            # -------------------------------------------------

            SolicitacaoEmpresa.objects.create(
                usuario=request.user,
                name=nome,
                website=website,
                status='pendente'
            )

            request.session[
                'empresa_solicitada_com_sucesso'
            ] = nome

            return redirect(
                'nova_empresa'
            )

    else:

        form = EmpresaForm()

    return render(
        request,
        'cadastro/empresas/nova.html',
        {
            'form': form,
            'semelhantes': semelhantes,
            'empresa_solicitada':
                empresa_solicitada,
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

            try:

                cargo = form.save()

            except IntegrityError:

                form.add_error(
                    'name',
                    _('Esse cargo já está cadastrado.')
                )

            else:

                return redirect(
                    f"{reverse('nova_candidatura')}"
                    f"?cargo={cargo.id}"
                )

    else:

        form = CargoForm()

    return render(
        request,
        'cadastro/cargos/novo.html',
        {
            'form': form
        }
    )


# =============================================================
# CADASTRO DE USUÁRIO
# =============================================================

def cadastro(request):

    if request.method == 'POST':

        form = CadastroForm(
            request.POST
        )

        if form.is_valid():

            nome = form.cleaned_data[
                'first_name'
            ]

            sobrenome = form.cleaned_data[
                'last_name'
            ]

            email = form.cleaned_data[
                'email'
            ]

            cpf = form.cleaned_data[
                'cpf'
            ]

            senha = form.cleaned_data[
                'senha'
            ]

            try:

                with transaction.atomic():

                    usuario = User.objects.create_user(
                        username=email,
                        email=email,
                        password=senha,
                        first_name=nome,
                        last_name=sobrenome
                    )

                    PerfilUsuario.objects.create(
                        usuario=usuario,
                        cpf=cpf
                    )

            except IntegrityError:

                form.add_error(
                    None,
                    _(
                        "Não foi possível criar a conta "
                        "com os dados informados. "
                        "Verifique seus dados e tente novamente."
                    )
                )

            else:

                login(
                    request,
                    usuario
                )

                return redirect(
                    'landing'
                )

    else:

        form = CadastroForm()

    return render(
        request,
        'cadastro/auth/cadastro.html',
        {
            'form': form
        }
    )


def login_usuario(request):

    if request.method == 'POST':

        email = (
            request.POST.get(
                'email'
            )
            or ''
        ).strip().lower()

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
                'landing'
            )

        return render(
            request,
            'cadastro/auth/login.html',
            {
                'erro':
                    'E-mail ou senha incorretos.'
            }
        )

    return render(
        request,
        'cadastro/auth/login.html'
    )


@login_required(login_url='login')
def logout_usuario(request):

    logout(
        request
    )

    return redirect(
        'login'
    )


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

                sugestao.usuario = (
                    request.user
                )

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
