# Job Tracker — Documentação do Projeto

## 1. Visão geral

**Job Tracker** é uma aplicação web construída com Django para organizar e acompanhar candidaturas a vagas de emprego.

A ideia central é transformar uma busca de emprego que normalmente fica espalhada entre planilhas, anotações e favoritos do navegador em um único sistema.

O projeto atualmente possui:

- Landing Page pública
- Cadastro de usuário
- Login e logout
- Sessões de autenticação do Django
- Candidaturas separadas por usuário
- Cadastro de empresas
- Cadastro de novas candidaturas
- PostgreSQL hospedado no Supabase
- Templates HTML com Django Templates
- CSS separado em arquivos estáticos
- Interface responsiva
- Primeira camada de identidade visual do produto

---

# 2. Tecnologias utilizadas

## Backend

### Python

É a linguagem principal da aplicação.

Ela executa a lógica do sistema, como:

- receber requisições
- validar formulários
- autenticar usuários
- consultar o banco
- salvar candidaturas
- renderizar páginas

### Django

É o framework web utilizado.

Ele organiza o projeto em partes como:

- Models
- Views
- URLs
- Templates
- Forms
- Static files
- Authentication

### PostgreSQL

É o banco de dados relacional utilizado pela aplicação.

### Supabase

O Supabase está sendo utilizado como serviço para hospedar o PostgreSQL.

---

# 3. Estrutura atual do projeto

Estrutura principal:

```text
supapaste/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
└── cadastro/
    │
    ├── migrations/
    │
    ├── templates/
    │   └── cadastro/
    │       ├── landing.html
    │       ├── login.html
    │       ├── cadastro.html
    │       ├── lista_candidaturas.html
    │       ├── nova_candidatura.html
    │       └── ...
    │
    ├── static/
    │   └── cadastro/
    │       ├── landing.css
    │       ├── auth.css
    │       └── style.css
    │
    ├── models.py
    ├── views.py
    ├── forms.py
    └── urls.py
```

---

# 4. O que cada parte faz

## `manage.py`

É o ponto de entrada dos comandos administrativos do Django.

Exemplos:

```powershell
python manage.py runserver
```

Inicia o servidor de desenvolvimento.

```powershell
python manage.py makemigrations
```

Cria arquivos de migration a partir das mudanças nos models.

```powershell
python manage.py migrate
```

Aplica as migrations no banco.

```powershell
python manage.py shell
```

Abre um shell Python com o Django carregado.

---

# 5. `config/`

É o pacote principal de configuração do projeto.

## `config/settings.py`

Contém configurações globais do Django, como:

- aplicativos instalados
- banco de dados
- arquivos estáticos
- templates
- middleware
- configurações de segurança
- configurações de autenticação

O app `cadastro` está instalado no projeto.

## `config/urls.py`

É a porta de entrada das URLs do projeto.

A configuração atual é:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastro.urls')),
]
```

Isso significa:

```text
/admin/
    ↓
Django Admin

/
    ↓
cadastro.urls
```

Ou seja, o `config/urls.py` encaminha as requisições para as URLs do app.

---

# 6. `cadastro/`

É o app principal do Job Tracker.

Ele concentra a lógica relacionada a:

- empresas
- candidaturas
- usuários
- autenticação
- páginas da aplicação

---

# 7. Modelos do banco

## `Empresa`

Modelo atual:

```python
class Empresa(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### Significado dos campos

### `name`

```python
models.CharField(max_length=200)
```

Armazena o nome da empresa.

`CharField` é utilizado para textos curtos.

`max_length=200` limita o tamanho máximo do texto.

### `city`

Armazena a cidade.

### `state`

Armazena a UF.

Foi definido:

```python
max_length=2
```

porque uma UF brasileira possui duas letras, como:

```text
DF
SP
RJ
MG
```

### `website`

Armazena a URL da empresa.

```python
blank=True
```

significa que o campo pode ficar vazio no formulário.

### `created_at`

```python
auto_now_add=True
```

faz o Django gravar automaticamente a data/hora de criação do registro.

---

# 8. Modelo `Candidatura`

O modelo de candidatura possui atualmente campos para:

- empresa
- usuário
- cargo
- data da candidatura
- salário
- link da vaga
- modalidade
- status
- observações
- último contato
- data de criação

Estrutura conceitual:

```text
Candidatura
│
├── empresa
├── usuario
├── cargo
├── data_candidatura
├── salario
├── link_vaga
├── modalidade
├── status
├── observacoes
├── ultimo_contato
└── created_at
```

---

# 9. Relação entre `Candidatura` e `Empresa`

A candidatura possui:

```python
empresa = models.ForeignKey(
    Empresa,
    on_delete=models.CASCADE,
    related_name='candidaturas'
)
```

Isso significa que várias candidaturas podem apontar para uma mesma empresa.

Exemplo:

```text
Google
│
├── Analista de QA
├── Analista de Dados
└── Desenvolvedor Jr
```

## `ForeignKey`

É uma relação entre tabelas.

A tabela `Candidatura` guarda uma referência para a empresa.

## `on_delete=models.CASCADE`

Determina o que acontece quando a empresa relacionada é excluída.

Com `CASCADE`, suas candidaturas relacionadas também seriam excluídas.

Essa decisão precisa ser considerada com cuidado em uma aplicação real.

---

# 10. Relação entre `Candidatura` e usuário

O campo foi adicionado:

```python
usuario = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='candidaturas',
    null=True,
    blank=True
)
```

Esse campo é responsável por separar as candidaturas entre usuários.

Conceito:

```text
Usuário Henrique
    ↓
Candidatura A
Candidatura B

Usuário Teste2
    ↓
Candidatura C
Candidatura D
```

## Por que `ForeignKey`?

Porque um usuário pode possuir várias candidaturas.

A relação é:

```text
1 usuário
   ↓
N candidaturas
```

Isso é uma relação **um-para-muitos**.

## Por que `null=True`?

O campo foi criado depois de já existirem candidaturas antigas.

O Django não sabia automaticamente a qual usuário aquelas candidaturas pertenciam.

Por isso, durante a implementação, foi permitido:

```text
usuario_id = NULL
```

para os registros antigos.

### Estado atual

O próximo passo, depois da limpeza ou atribuição das candidaturas antigas, pode ser transformar esse campo em obrigatório.

---

# 11. Migrations

Quando o campo `usuario` foi adicionado ao modelo, executamos:

```powershell
python manage.py makemigrations
```

O Django criou:

```text
cadastro/migrations/0003_candidatura_usuario.py
```

Esse arquivo descreve a alteração.

Depois executamos:

```powershell
python manage.py migrate
```

Resultado:

```text
Applying cadastro.0003_candidatura_usuario... OK
```

Isso significa que a alteração foi aplicada ao PostgreSQL.

## Regra mental

```text
models.py
    ↓
makemigrations
    ↓
arquivo de migration
    ↓
migrate
    ↓
banco de dados
```

`makemigrations` prepara a alteração.

`migrate` aplica a alteração.

---

# 12. Autenticação

O projeto usa o sistema de autenticação nativo do Django.

Foram utilizados:

```python
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
```

## Cadastro

O usuário informa:

- nome
- e-mail
- senha

O sistema cria um `User` do Django.

A criação utiliza:

```python
User.objects.create_user(
    username=email,
    email=email,
    password=senha,
    first_name=nome
)
```

A senha não é armazenada como texto puro pelo Django.

O sistema de autenticação do Django faz o tratamento adequado da senha.

---

# 13. Login

O login recebe:

```text
email
senha
```

A aplicação executa:

```python
usuario = authenticate(
    request,
    username=email,
    password=senha
)
```

Se as credenciais forem válidas:

```python
login(request, usuario)
```

A partir desse momento o Django sabe qual usuário está associado à sessão atual.

Isso permite:

```python
request.user
```

Exemplo:

```text
login do teste1
    ↓
request.user = teste1

login do teste2
    ↓
request.user = teste2
```

---

# 14. Logout

A função de logout é:

```python
def logout_usuario(request):
    logout(request)
    return redirect('login')
```

Fluxo:

```text
clique em SAIR
    ↓
/logout/
    ↓
logout(request)
    ↓
sessão encerrada
    ↓
/login/
```

---

# 15. Proteção das páginas

Foi utilizado:

```python
@login_required(login_url='login')
```

Isso significa que a página exige autenticação.

Exemplo:

```python
@login_required(login_url='login')
def lista_candidaturas(request):
    ...
```

Se alguém tentar acessar sem estar logado:

```text
/candidaturas/
```

o Django manda a pessoa para:

```text
/login/
```

---

# 16. Separação das candidaturas por usuário

A lógica da listagem é:

```python
candidaturas = Candidatura.objects.filter(
    usuario=request.user
).order_by('-data_candidatura')
```

Isso é uma das partes mais importantes do projeto.

`objects.filter(...)` significa:

> buscar apenas registros que atendam ao critério informado.

Neste caso:

```python
usuario=request.user
```

significa:

> buscar somente candidaturas pertencentes ao usuário atualmente logado.

---

# 17. Salvando o usuário na candidatura

Na criação da candidatura, usamos:

```python
candidatura = form.save(commit=False)

candidatura.usuario = request.user

candidatura.save()
```

## Por que `commit=False`?

Normalmente:

```python
form.save()
```

já salva diretamente no banco.

Mas precisamos modificar a candidatura antes de salvar.

O fluxo é:

```text
form.save(commit=False)
        ↓
objeto criado na memória
        ↓
usuario = request.user
        ↓
save()
        ↓
banco
```

Isso permite adicionar o dono da candidatura automaticamente.

---

# 18. Views atuais

As principais views são:

## `landing`

Mostra a Landing Page.

```python
def landing(request):
    return render(request, 'cadastro/landing.html')
```

## `lista_empresas`

Lista empresas.

## `lista_candidaturas`

Lista somente as candidaturas do usuário atual.

## `nova_candidatura`

Exibe e processa o formulário de nova candidatura.

## `cadastro`

Cria um usuário e faz login automaticamente.

## `login_usuario`

Autentica o usuário.

## `logout_usuario`

Encerra a sessão.

---

# 19. URLs atuais

No app:

```python
urlpatterns = [
    path('', views.landing, name='landing'),

    path(
        'empresas/',
        views.lista_empresas,
        name='lista_empresas'
    ),

    path(
        'candidaturas/',
        views.lista_candidaturas,
        name='lista_candidaturas'
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
```

Mapa das páginas:

```text
/                       Landing Page
/login/                 Login
/cadastro/              Cadastro
/logout/                Logout
/candidaturas/          Lista de candidaturas
/candidaturas/nova/     Nova candidatura
/empresas/              Lista de empresas
```

---

# 20. Templates

Os templates são os arquivos HTML que o Django renderiza.

Eles usam Django Template Language.

Exemplo:

```django
{{ request.user.first_name }}
```

Isso acessa o nome do usuário atual.

Outro exemplo:

```django
{% url 'login' %}
```

pede ao Django para gerar a URL associada ao nome `login`.

---

# 21. Arquivos estáticos

O projeto começou a separar o CSS em arquivos próprios.

Estrutura:

```text
static/
└── cadastro/
    ├── landing.css
    ├── auth.css
    └── style.css
```

## `landing.css`

Responsável pela aparência da Landing Page.

## `auth.css`

Compartilhado pelas páginas:

- login
- cadastro

Isso evita duplicar CSS.

## `style.css`

Responsável pela interface da área de candidaturas.

---

# 22. HTML x CSS

Uma regra importante adotada no projeto:

### HTML

Define estrutura e conteúdo.

Exemplo:

```html
<h1>JOB TRACKER</h1>
```

### CSS

Define aparência.

Exemplo:

```css
font-size: 20px;
font-weight: 900;
letter-spacing: 4px;
```

A separação facilita manutenção.

Em vez de colocar dezenas de regras dentro do HTML, cada responsabilidade fica em seu arquivo.

---

# 23. Landing Page

A Landing Page é pública.

Ela apresenta:

- marca Job Tracker
- proposta do produto
- chamada principal
- botões de cadastro/login
- preview de dashboard
- recursos
- como funciona
- chamada final para cadastro

A rota é:

```text
/
```

O sistema diferencia automaticamente visitante e usuário autenticado.

Exemplo:

```django
{% if request.user.is_authenticated %}
```

Permite mostrar um botão como:

```text
Meu painel
```

para usuários logados.

Para visitantes:

```text
Entrar
Criar conta
```

---

# 24. Identidade visual

A identidade atual segue uma direção de SaaS moderno:

- fundo claro
- preto/cinza escuro
- azul/roxo como destaque
- cantos arredondados
- sombras suaves
- bastante espaço em branco
- hover e transições
- responsividade

O objetivo é fazer o projeto parecer um produto real, e não apenas uma tela CRUD.

---

# 25. Fluxo completo do sistema

## Visitante

```text
/
 ↓
Landing Page
 ↓
Criar conta
 ↓
Cadastro
 ↓
Usuário criado
 ↓
Login automático
 ↓
/candidaturas/
```

## Usuário existente

```text
/
 ↓
Entrar
 ↓
/login/
 ↓
authenticate()
 ↓
login()
 ↓
/candidaturas/
```

## Nova candidatura

```text
/candidaturas/
 ↓
Nova candidatura
 ↓
/candidaturas/nova/
 ↓
Formulário
 ↓
form.save(commit=False)
 ↓
usuario = request.user
 ↓
save()
 ↓
/candidaturas/
```

## Logout

```text
/candidaturas/
 ↓
SAIR
 ↓
/logout/
 ↓
logout()
 ↓
/login/
```

---

# 26. Banco de dados — visão conceitual

Estrutura simplificada:

```text
User
│
├── id
├── username
├── email
├── first_name
└── password
       │
       │ 1:N
       ▼
Candidatura
│
├── id
├── usuario_id
├── empresa_id
├── cargo
├── data_candidatura
├── salario
├── link_vaga
├── modalidade
├── status
├── observacoes
├── ultimo_contato
└── created_at
       │
       │ N:1
       ▼
Empresa
├── id
├── name
├── city
├── state
├── website
└── created_at
```

---

# 27. Decisão importante: um banco só

O projeto não cria um banco de dados PostgreSQL separado para cada usuário.

Usamos um banco único.

A separação acontece através do relacionamento:

```text
Candidatura.usuario_id
```

Exemplo:

```text
User id 1
    ↓
Candidatura 10
Candidatura 11

User id 2
    ↓
Candidatura 20
Candidatura 21
```

Esse modelo é o padrão para muitos sistemas web.

---

# 28. Estado atual

### Funcionalidades concluídas

- [x] Projeto Django funcionando
- [x] PostgreSQL/Supabase conectado
- [x] Model Empresa
- [x] Model Candidatura
- [x] Cadastro
- [x] Login
- [x] Logout
- [x] Sessão de usuário
- [x] Proteção com `login_required`
- [x] Candidaturas associadas a usuário
- [x] Filtro de candidaturas por usuário
- [x] Landing Page
- [x] CSS separado
- [x] Identidade visual inicial
- [x] Layout responsivo

---

# 29. Pendências técnicas

## Candidaturas antigas

Existem registros criados antes do relacionamento com usuário.

Esses registros podem estar com:

```text
usuario = NULL
```

Eles precisam ser tratados.

Possibilidades:

- apagar dados de teste
- atribuir a um usuário
- manter como registros sem dono apenas temporariamente

Depois disso, pode ser interessante tornar o campo obrigatório:

```python
null=False
blank=False
```

---

# 30. Próximos passos planejados

## Interface

A próxima grande tarefa é refazer:

```text
/candidaturas/
```

para seguir a mesma identidade visual da Landing Page e do Login/Cadastro.

Objetivo:

```text
Dashboard moderno
        ↓
métricas
        ↓
lista de candidaturas
        ↓
status visuais
        ↓
ações
```

## CRUD completo

Adicionar:

- editar candidatura
- excluir candidatura
- confirmação antes de excluir

## Dashboard

Adicionar indicadores como:

```text
TOTAL
ENTREVISTAS
TESTES
APROVADAS
RECUSADAS
```

Todos calculados somente a partir das candidaturas do usuário logado.

## Filtros

Permitir filtrar por:

- status
- modalidade
- empresa
- período

## Melhorias futuras

- pesquisa
- ordenação
- gráficos
- notificações
- histórico de alterações
- recuperação de senha
- validação de e-mail
- publicação online
- domínio próprio
- melhoria de segurança
- testes automatizados

---

# 31. Comandos importantes

Iniciar servidor:

```powershell
python manage.py runserver
```

Criar migration:

```powershell
python manage.py makemigrations
```

Aplicar migration:

```powershell
python manage.py migrate
```

Shell Django:

```powershell
python manage.py shell
```

Criar superusuário:

```powershell
python manage.py createsuperuser
```

---

# 32. Regra de estudo adotada no projeto

A partir desta etapa, o objetivo não é apenas terminar o Job Tracker.

O objetivo também é aprender a construir aplicações Django.

Para cada mudança de código, devemos entender:

1. O que o código faz.
2. Por que ele é necessário.
3. O significado dos parâmetros.
4. Como uma parte conversa com outra.
5. O que aconteceria se aquela linha fosse removida.
6. Como poderíamos implementar a mesma ideia de outra forma.

Exemplo:

```css
font-size: 20px;
```

Não basta saber que "aumenta o texto".

É necessário entender:

- `font-size` controla o tamanho da fonte.
- `20px` é o valor escolhido.
- o valor não é uma regra universal.
- a escolha depende da hierarquia visual.
- títulos normalmente são maiores que textos auxiliares.
- aumentar demais um elemento pode quebrar a hierarquia da interface.

A intenção é migrar progressivamente de:

```text
"me dê o código"
```

para:

```text
"me deixe tentar construir"
```

e finalmente:

```text
"eu consigo construir sozinho"
```

---

# 33. Filosofia do projeto

O Job Tracker está sendo construído com duas metas simultâneas:

### Produto

Uma aplicação visualmente agradável, funcional e apresentável.

### Aprendizado

Um projeto que ensina:

- Python
- Django
- PostgreSQL
- modelagem de banco
- autenticação
- HTTP
- HTML
- CSS
- JavaScript futuramente
- Git/GitHub futuramente
- deploy futuramente

Por isso, as decisões devem ser explicadas e não apenas copiadas.

---

# 34. Visão de arquitetura atual

```text
                    NAVEGADOR
                        │
                        ▼
                    Django URLs
                        │
          ┌─────────────┴──────────────┐
          ▼                            ▼
       Landing                     Auth / App
          │                            │
          ▼                            ▼
      Templates                      Views
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼            ▼
                        Forms       Models       Auth
                                       │
                                       ▼
                                  PostgreSQL
                                       │
                                       ▼
                                    Supabase
```

---

# 35. Próximo marco

Antes de adicionar novas funcionalidades, a prioridade imediata é:

```text
1. Redesenhar /candidaturas/
2. Criar dashboard
3. Adicionar editar/excluir
4. Criar filtros
5. Melhorar experiência do usuário
```

Esse será o momento em que o Job Tracker passa de uma aplicação funcional para uma aplicação com aparência de produto.

---

## Observação

Esta documentação representa o estado do projeto construído e discutido até o momento. Ela deve ser atualizada sempre que uma nova funcionalidade ou mudança arquitetural importante for adicionada.

Teste de integração com GitHub.