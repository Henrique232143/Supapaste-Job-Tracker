from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Empresa, Candidatura
from .forms import CandidaturaForm, CadastroForm


def landing(request):
    return render(request, 'cadastro/landing.html')


@login_required(login_url='login')
def lista_empresas(request):
    empresas = Empresa.objects.all()

    return render(request, 'cadastro/lista_empresas.html', {
        'empresas': empresas
    })


@login_required(login_url='login')
def lista_candidaturas(request):
    candidaturas = Candidatura.objects.filter(
        usuario=request.user
    ).order_by('-data_candidatura')

    return render(request, 'cadastro/lista_candidaturas.html', {
        'candidaturas': candidaturas
    })


@login_required(login_url='login')
def nova_candidatura(request):
    if request.method == 'POST':
        form = CandidaturaForm(request.POST)

        if form.is_valid():
            candidatura = form.save(commit=False)

            candidatura.usuario = request.user

            candidatura.save()

            return redirect('lista_candidaturas')

    else:
        form = CandidaturaForm()

    return render(request, 'cadastro/nova_candidatura.html', {
        'form': form
    })


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            usuario = User.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome
            )

            login(request, usuario)

            return redirect('lista_candidaturas')

    else:
        form = CadastroForm()

    return render(request, 'cadastro/cadastro.html', {
        'form': form
    })


def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = authenticate(
            request,
            username=email,
            password=senha
        )

        if usuario is not None:
            login(request, usuario)

            return redirect('lista_candidaturas')

        return render(request, 'cadastro/login.html', {
            'erro': 'E-mail ou senha incorretos.'
        })

    return render(request, 'cadastro/login.html')


@login_required(login_url='login')
def logout_usuario(request):
    logout(request)

    return redirect('login')

