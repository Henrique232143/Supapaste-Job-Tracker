# Job Tracker — Documentação do Projeto

## 1. Visão geral

**Job Tracker** é uma aplicação web construída com Django para organizar e acompanhar candidaturas a vagas de emprego.

A ideia central é transformar uma busca de emprego que normalmente fica espalhada entre planilhas, anotações, favoritos do navegador e diferentes sites em um único sistema.

O projeto evoluiu de um CRUD simples de empresas e candidaturas para uma aplicação com uma estrutura mais próxima de um produto real, incluindo:

* Landing Page pública
* Cadastro de usuário
* Login e logout
* Sessões de autenticação do Django
* Candidaturas separadas por usuário
* Cadastro e reutilização de empresas
* Catálogo global de empresas
* Catálogo de cargos
* Normalização de nomes
* Tratamento de empresas duplicadas ou semelhantes
* Sistema de aliases de empresas
* Detalhamento individual de uma candidatura
* Criação rápida de empresa durante o cadastro da candidatura
* Criação rápida de cargo
* Campo para local da vaga
* Camada de serviços para concentrar regras de negócio
* Comando administrativo para manutenção de catálogos
* Internacionalização inicial
* Seletor de idioma
* Interface mais consistente entre as páginas
* PostgreSQL hospedado no Supabase
* Versionamento com Git/GitHub

---

# 2. Tecnologias utilizadas

## Backend

### Python

É a linguagem principal da aplicação.

Ela executa a lógica do sistema, como:

* receber requisições
* validar formulários
* autenticar usuários
* consultar o banco
* aplicar regras de negócio
* salvar registros
* renderizar páginas

### Django

É o framework web utilizado.

Ele organiza o projeto em partes como:

* Models
* Views
* URLs
* Templates
* Forms
* Static files
* Authentication
* Migrations
* Management Commands
* Internationalization

### PostgreSQL

É o banco de dados relacional utilizado pela aplicação.

### Supabase

O Supabase está sendo utilizado como serviço para hospedar o PostgreSQL.

### HTML / Django Templates

Responsáveis pela estrutura das páginas e pela renderização dinâmica dos dados.

### CSS

Responsável pela identidade visual e pelos layouts das páginas.

### Git / GitHub

Utilizados para versionamento do projeto.

A branch atual de desenvolvimento é:

```text
melhorar-cards-vagas
```

---

# 3. Estrutura atual do projeto

A estrutura evoluiu bastante desde a primeira versão.

Estrutura principal:

```text
Supapaste/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── locale/
│   ├── de/
│   ├── en/
│   ├── ja/
│   └── pt_PT/
│
└── cadastro/
    │
    ├── management/
    │   └── commands/
    │       └── catalogos.py
    │
    ├── migrations/
    │   ├── 0001_initial.py
    │   ├── 0002_...
    │   ├── 0003_candidatura_usuario.py
    │   ├── 0004_cargo_empresa_name_normalized.py
    │   ├── 0005_empresaalias.py
    │   ├── 0006_candidatura_local_vaga.py
    │   └── 0007_alter_empresa_city_alter_empresa_state_and_more.py
    │
    ├── templates/
    │   └── cadastro/
    │       ├── landing.html
    │       ├── login.html
    │       ├── cadastro.html
    │       ├── candidaturas.html
    │       ├── detalhe_candidatura.html
    │       ├── nova_candidatura.html
    │       ├── nova_empresa.html
    │       ├── novo_cargo.html
    │       ├── ...
    │       ├── locale/
    │       └── partials/
    │           └── language_selector.html
    │
    ├── static/
    │   └── cadastro/
    │       ├── candidaturas.css
    │       ├── detalhe_candidatura.css
    │       ├── language-switcher.css
    │       ├── nova_candidatura.css
    │       ├── nova_empresa.css
    │       ├── novo_cargo.css
    │       ├── landing.css
    │       ├── auth.css
    │       └── ...
    │
    ├── models.py
    ├── forms.py
    ├── servicos.py
    ├── views.py
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

Aplica as migrations ao banco de dados.

```powershell
python manage.py shell
```

Abre um shell Python com o ambiente Django carregado.

Também foi adicionada uma estrutura de **Management Commands** para tarefas internas do projeto.

---

# 5. `config/`

É o pacote principal de configuração do projeto.

## `config/settings.py`

Contém as configurações globais do Django, incluindo:

* aplicativos instalados
* banco de dados
* templates
* arquivos estáticos
* middleware
* autenticação
* internacionalização
* configurações de idioma
* configurações de segurança

## `config/urls.py`

É a porta de entrada das URLs do projeto.

Configuração conceitual:

```python
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

---

# 6. `cadastro/`

É o app principal do Job Tracker.

Ele concentra a lógica relacionada a:

* empresas
* aliases
* cargos
* candidaturas
* usuários
* autenticação
* formulários
* catálogos
* páginas da aplicação
* regras de negócio

---

# 7. Modelos do banco

A modelagem do banco evoluiu significativamente.

Atualmente, o projeto trabalha conceitualmente com:

```text
User
    │
    └── Candidaturas
             │
             ├── Empresa
             ├── Cargo
             └── dados da vaga

Empresa
    │
    └── Aliases

Cargo
    │
    └── Empresa
```

---

# 8. Modelo `Empresa`

A entidade `Empresa` representa as empresas utilizadas no Job Tracker.

Ela possui dados relacionados à identificação da empresa e à sua localização.

A aplicação também passou a trabalhar com **normalização de nomes**, permitindo identificar melhor empresas que aparecem escritas de maneiras diferentes.

Exemplo conceitual:

```text
Serasa Experian
SERASA EXPERIAN
Serasa
Serasa Experian Ltda.
```

Podem representar a mesma empresa.

A normalização existe para ajudar o sistema a enxergar essa equivalência.

---

# 9. Normalização

Uma das mudanças mais importantes da evolução recente foi a criação da lógica de **normalização**.

Normalizar significa transformar diferentes representações de um texto em uma forma mais consistente para comparação.

Exemplo conceitual:

```text
"Serasa Experian"
"SERASA EXPERIAN"
" serasa experian "
```

podem ser transformados em uma representação equivalente para comparação.

A normalização é importante porque:

* reduz duplicidades
* melhora pesquisas
* facilita identificação de empresas semelhantes
* permite reutilizar empresas existentes
* cria uma base melhor para automações futuras

A migration:

```text
0004_cargo_empresa_name_normalized.py
```

faz parte dessa evolução.

---

# 10. Modelo `EmpresaAlias`

Foi criado o modelo:

```text
EmpresaAlias
```

Seu objetivo é representar nomes alternativos associados a uma empresa principal.

Conceito:

```text
Empresa
Serasa Experian
        │
        ├── Serasa
        ├── SERASA
        └── Serasa Experian S.A.
```

Isso permite separar:

```text
nome oficial/canônico
```

de:

```text
nomes alternativos usados na prática
```

Essa estrutura é importante para evitar que a mesma empresa seja cadastrada diversas vezes.

A migration relacionada é:

```text
0005_empresaalias.py
```

---

# 11. Empresas semelhantes e duplicidade

O projeto passou a tratar a criação de empresas de maneira mais inteligente.

Em vez de simplesmente verificar se uma string é exatamente igual à outra, o sistema pode trabalhar com:

```text
nome informado
      ↓
normalização
      ↓
comparação
      ↓
empresa existente?
      ↓
sim / não / semelhante
```

Isso permite construir uma experiência mais próxima de:

> "Essa empresa talvez já exista no catálogo."

Essa camada é fundamental para que o catálogo global não fique cheio de duplicações.

---

# 12. Modelo `Cargo`

O projeto passou a ter uma entidade própria para cargos.

O objetivo é evitar que os cargos sejam tratados apenas como texto solto espalhado pelas candidaturas.

Conceito:

```text
Empresa
   ↓
Cargo
   ├── Analista de Qualidade
   ├── Analista de Dados
   └── Desenvolvedor Júnior
```

O modelo também passou a participar da lógica de normalização.

A migration:

```text
0004_cargo_empresa_name_normalized.py
```

está relacionada a essa evolução.

---

# 13. Cargo e candidatura

É importante diferenciar duas coisas:

### Cadastro de Cargo

O sistema já possui uma entidade de cargo e mecanismos para trabalhar com o catálogo.

### FK definitiva na candidatura

A associação definitiva entre:

```text
Candidatura
       ↓
Cargo
```

como uma `ForeignKey` real ainda faz parte da evolução arquitetural.

Portanto, o projeto já possui a estrutura de cargos, mas essa etapa ainda pode ser refinada para eliminar completamente a dependência de cargo como texto dentro da candidatura.

---

# 14. Modelo `Candidatura`

A candidatura continua sendo a principal entidade operacional do sistema.

Ela reúne informações como:

* empresa
* usuário
* cargo
* data da candidatura
* salário
* link da vaga
* modalidade
* status
* observações
* último contato
* local da vaga
* data de criação

Estrutura conceitual:

```text
Candidatura
│
├── usuario
├── empresa
├── cargo
├── data_candidatura
├── salario
├── link_vaga
├── modalidade
├── status
├── local_vaga
├── observacoes
├── ultimo_contato
└── created_at
```

A migration:

```text
0006_candidatura_local_vaga.py
```

representa a adição relacionada ao local da vaga.

---

# 15. Relação entre `Candidatura` e `Empresa`

A candidatura está relacionada à empresa.

Conceito:

```text
Empresa
   │
   ├── Candidatura A
   ├── Candidatura B
   └── Candidatura C
```

Uma mesma empresa pode aparecer em diversas candidaturas.

Isso permite que o sistema tenha:

```text
1 Empresa
   ↓
N Candidaturas
```

em vez de criar uma nova empresa para cada candidatura.

---

# 16. Relação entre `Candidatura` e usuário

A candidatura possui associação com o usuário logado.

Conceito:

```text
Usuário Henrique
    ↓
Candidatura A
Candidatura B

Usuário Teste
    ↓
Candidatura C
Candidatura D
```

Isso garante que cada usuário veja suas próprias candidaturas.

A filtragem continua baseada no usuário autenticado.

---

# 17. Catálogo global

O sistema deixou de tratar empresas e cargos somente como informações digitadas em uma candidatura.

Foi criada uma lógica de **catálogo global**.

A ideia é:

```text
Catálogo
│
├── Empresas
│
└── Cargos
```

Esse catálogo pode ser reutilizado por diferentes usuários.

Isso é diferente das candidaturas, que continuam sendo privadas de cada usuário.

Exemplo:

```text
Catálogo global
    ↓
Google
Meta
Serasa Experian
Deloitte
Microsoft

Usuário Henrique
    ↓
Candidatura na Serasa

Usuário Teste
    ↓
Candidatura na Microsoft
```

O catálogo funciona como uma base compartilhada de entidades.

---

# 18. Comando `catalogos.py`

Foi criada a estrutura:

```text
cadastro/
└── management/
    └── commands/
        └── catalogos.py
```

Esse tipo de arquivo permite criar comandos próprios do Django.

A existência desse comando prepara o sistema para tarefas como:

* manutenção de catálogos
* criação de registros
* atualização de dados
* normalização
* operações administrativas
* preparação de dados

Isso também tira determinadas tarefas de dentro das views.

---

# 19. `servicos.py`

Foi criada uma camada:

```text
cadastro/servicos.py
```

A ideia é concentrar regras de negócio em um lugar próprio, evitando colocar toda a inteligência da aplicação dentro de:

```text
views.py
```

A arquitetura passa a caminhar para:

```text
View
  ↓
Service
  ↓
Model
  ↓
Banco
```

Isso melhora a organização do projeto e facilita futuras automações.

---

# 20. Autenticação

O projeto continua utilizando o sistema nativo de autenticação do Django.

Foram utilizados:

```python
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
```

## Cadastro

O usuário informa os dados necessários e o sistema cria um usuário Django.

A senha é tratada pelo sistema de autenticação do próprio Django, em vez de ser armazenada em texto puro.

---

# 21. Login

O login recebe:

```text
email
senha
```

O sistema autentica o usuário com:

```python
authenticate()
```

Se as credenciais forem válidas:

```python
login()
```

A partir daí:

```python
request.user
```

representa o usuário atualmente autenticado.

---

# 22. Logout

O fluxo continua sendo:

```text
/candidaturas/
      ↓
Sair
      ↓
/logout/
      ↓
logout()
      ↓
/login/
```

---

# 23. Proteção das páginas

Páginas privadas continuam utilizando:

```python
@login_required(login_url='login')
```

Isso protege áreas como o painel e as candidaturas.

O objetivo é impedir acesso aos dados sem autenticação.

---

# 24. Views atuais

As views cresceram junto com a aplicação.

Entre as principais responsabilidades estão:

## Landing

Exibe a página pública inicial.

## Empresas

Lista e trabalha com empresas do catálogo.

## Candidaturas

Exibe as candidaturas do usuário.

## Nova candidatura

Exibe e processa o cadastro de uma candidatura.

## Detalhe da candidatura

Foi criada uma página específica para visualizar uma candidatura individual.

Exemplo:

```text
/candidaturas/
       ↓
seleciona candidatura
       ↓
detalhe da candidatura
```

## Cadastro

Cria novos usuários.

## Login

Autentica usuários.

## Logout

Encerra sessões.

## Empresa

Foi adicionada uma tela própria para criação de empresa:

```text
nova_empresa.html
```

## Cargo

Também foi adicionada uma tela própria para criação de cargo:

```text
novo_cargo.html
```

---

# 25. Nova candidatura

O fluxo de criação ficou mais completo.

Anteriormente, a candidatura era essencialmente um formulário isolado.

Agora a experiência pode envolver:

```text
Nova candidatura
       ↓
Empresa
   ├── existente
   ├── semelhante
   └── nova empresa
       ↓
Cargo
   ├── existente
   └── novo cargo
       ↓
Dados da vaga
       ↓
Salvar
```

Isso aproxima o sistema de uma experiência real de produto.

---

# 26. Detalhe da candidatura

Foi criada uma página específica:

```text
detalhe_candidatura.html
```

com CSS próprio:

```text
detalhe_candidatura.css
```

O objetivo é separar a visualização detalhada de uma candidatura da listagem geral.

Isso cria uma arquitetura mais organizada:

```text
Lista
  ↓
Resumo

Detalhe
  ↓
Informações completas
```

Essa separação será especialmente útil quando forem adicionadas ações como:

* editar
* excluir
* histórico
* movimentação de status
* observações
* contatos

---

# 27. Templates

Os templates passaram a cobrir uma quantidade maior de funcionalidades.

Entre os principais:

```text
landing.html
login.html
cadastro.html
candidaturas.html
detalhe_candidatura.html
nova_candidatura.html
nova_empresa.html
novo_cargo.html
```

Também foi criada a estrutura:

```text
partials/
└── language_selector.html
```

Isso permite reutilizar componentes de interface sem duplicar HTML.

---

# 28. Arquivos estáticos

A organização do CSS ficou mais modular.

Entre os arquivos atuais:

```text
candidaturas.css
detalhe_candidatura.css
language-switcher.css
nova_candidatura.css
nova_empresa.css
novo_cargo.css
```

Além dos arquivos já existentes para:

```text
landing
auth
```

A ideia é que cada área tenha seu estilo próprio quando necessário, reduzindo conflitos entre páginas.

---

# 29. Interface consistente

A interface passou a seguir uma identidade visual mais definida.

Direção adotada:

* fundo claro
* superfícies brancas
* tons escuros para textos
* roxo/índigo como destaque
* bordas suaves
* sombras discretas
* cantos arredondados
* bastante espaço em branco
* hierarquia visual clara
* aparência de produto SaaS
* responsividade

O objetivo deixou de ser apenas:

```text
"fazer funcionar"
```

e passou a ser:

```text
"fazer funcionar + parecer um produto"
```

---

# 30. Internacionalização

O projeto começou a receber suporte à internacionalização do Django.

Foram criadas estruturas de tradução para:

```text
de
en
ja
pt_PT
```

Além disso, foi criada uma interface própria de seleção de idioma.

Estrutura:

```text
locale/
├── de/
├── en/
├── ja/
└── pt_PT/
```

e também:

```text
cadastro/templates/cadastro/locale/
```

Essa etapa prepara o Job Tracker para trabalhar com múltiplos idiomas sem precisar duplicar templates inteiros.

---

# 31. Sistema de idiomas

Foi adicionada uma estrutura visual específica para o seletor de idioma:

```text
language_selector.html
language-switcher.css
```

A ideia é centralizar a seleção do idioma em um componente reutilizável.

Arquitetura conceitual:

```text
Usuário
   ↓
Seleciona idioma
   ↓
Django
   ↓
Sistema de tradução
   ↓
Interface no idioma selecionado
```

---

# 32. Migrations recentes

As últimas mudanças estruturais geraram novas migrations.

## `0004_cargo_empresa_name_normalized.py`

Relacionada à evolução de cargos, empresas e normalização de nomes.

## `0005_empresaalias.py`

Criação da estrutura de aliases de empresas.

## `0006_candidatura_local_vaga.py`

Adição do local associado à vaga/candidatura.

## `0007_alter_empresa_city_alter_empresa_state_and_more.py`

Atualizações adicionais na estrutura de empresa e outros ajustes de schema.

A sequência atual mostra que o banco está evoluindo junto com a arquitetura da aplicação.

---

# 33. Regra mental sobre migrations

A lógica continua sendo:

```text
models.py
    ↓
makemigrations
    ↓
arquivo de migration
    ↓
migrate
    ↓
PostgreSQL
```

É importante lembrar:

`makemigrations`

prepara a alteração.

`migrate`

aplica a alteração ao banco.

---

# 34. Fluxo atual do sistema

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
Login
 ↓
Área de candidaturas
```

## Usuário existente

```text
/
 ↓
Login
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
Empresa
 ↓
Empresa existente?
 ├── sim
 ├── semelhante
 └── nova
 ↓
Cargo
 ↓
Dados da vaga
 ↓
Salvar
 ↓
Candidatura criada
```

## Visualização

```text
/candidaturas/
 ↓
Seleciona candidatura
 ↓
detalhe_candidatura
```

---

# 35. Banco de dados — visão conceitual atual

```text
                         User
                          │
                          │ 1:N
                          ▼
                     Candidatura
                    /      │      \
                   /       │       \
                  ▼        ▼        ▼
             Empresa     Cargo    dados
                │
                │
                ▼
          EmpresaAlias
```

O catálogo funciona como uma base global de entidades:

```text
Empresa
   ↓
Catálogo global

Cargo
   ↓
Catálogo global
```

Enquanto:

```text
Candidatura
   ↓
pertence a um usuário específico
```

---

# 36. Separação entre catálogo global e dados do usuário

Essa é uma decisão arquitetural importante.

### Catálogo

É compartilhado.

Exemplo:

```text
Empresa:
Serasa Experian
```

pode existir uma única vez no catálogo.

### Candidatura

É individual.

Exemplo:

```text
Henrique
   ↓
Candidatura na Serasa
```

Outro usuário poderia ter:

```text
Outro usuário
   ↓
Candidatura na Serasa
```

Os dois reutilizam a mesma entidade `Empresa`, mas possuem candidaturas diferentes.

---

# 37. Estado atual

## Base

* [x] Projeto Django funcionando
* [x] PostgreSQL/Supabase conectado
* [x] Estrutura de app
* [x] Migrations
* [x] Git/GitHub

## Usuários

* [x] Cadastro
* [x] Login
* [x] Logout
* [x] Sessão
* [x] `request.user`
* [x] `login_required`

## Candidaturas

* [x] Cadastro
* [x] Associação ao usuário
* [x] Listagem
* [x] Status
* [x] Data
* [x] Salário
* [x] Link da vaga
* [x] Modalidade
* [x] Observações
* [x] Último contato
* [x] Local da vaga
* [x] Tela de detalhe

## Empresas

* [x] Model `Empresa`
* [x] Cadastro
* [x] Catálogo global
* [x] Normalização
* [x] Identificação de semelhantes
* [x] Aliases
* [x] Tela de nova empresa

## Cargos

* [x] Estrutura de `Cargo`
* [x] Catálogo de cargos
* [x] Normalização
* [x] Tela de novo cargo
* [ ] FK definitiva de `Cargo` em `Candidatura`

## Interface

* [x] Landing Page
* [x] Login
* [x] Cadastro
* [x] Área de candidaturas
* [x] Tela de detalhe
* [x] Tela de nova empresa
* [x] Tela de novo cargo
* [x] CSS separado
* [x] Identidade visual consistente
* [x] Seletor de idioma
* [x] Base de internacionalização

## Arquitetura

* [x] Camada de services
* [x] Management Command para catálogos
* [x] Organização de templates
* [x] Partial reutilizável
* [x] Estrutura global de catálogos

---

# 38. Pendências técnicas

## Candidaturas antigas

Ainda pode existir a necessidade de tratar registros criados antes da associação das candidaturas aos usuários.

Esses registros podem ter:

```text
usuario = NULL
```

Eles devem ser analisados antes de tornar a relação definitivamente obrigatória.

---

# 39. Próxima grande etapa

A prioridade atual deixa de ser a construção da base de empresas semelhantes e aliases, porque essa camada já foi implementada.

O próximo passo passa a ser o **CRUD completo das entidades já existentes**.

Prioridade imediata:

```text
1. Editar candidatura
2. Excluir candidatura
3. Confirmação de exclusão
4. Revisar edição/exclusão de empresas
5. Revisar edição/exclusão de cargos
```

---

# 40. Roadmap atualizado

## ✅ CONCLUÍDO

```text
✅ Base Django
✅ PostgreSQL / Supabase
✅ Login / usuários
✅ Sessões
✅ Proteção de páginas
✅ Candidaturas
✅ Empresas
✅ Catálogo global
✅ Cargos
✅ Normalização
✅ Duplicidade
✅ Empresas semelhantes
✅ Aliases de empresas
✅ Detalhe da candidatura
✅ Cadastro rápido de empresa
✅ Cadastro rápido de cargo
✅ Local da vaga
✅ Camada de serviços
✅ Management Command de catálogos
✅ Interface consistente
✅ CSS modularizado
✅ Internacionalização inicial
✅ Seletor de idioma
✅ Git / GitHub
```

---

## 🔵 AGORA

### CRUD

```text
→ Editar candidatura
→ Excluir candidatura
→ Confirmação de exclusão
→ Revisar edição/exclusão de empresa
→ Revisar edição/exclusão de cargo
```

---

## 🔵 DEPOIS

### Catálogo

```text
→ Catálogo de empresas com interface completa
→ Busca de empresas
→ Busca de cargos
→ Melhor gerenciamento de aliases
→ Melhor tratamento de duplicidades
```

### Estrutura de cargos

```text
→ FK real de Cargo em Candidatura
→ Relacionamento definitivo Empresa → Cargo
→ Reutilização de cargos do catálogo
```

### Pesquisa e filtros

```text
→ Filtro por status
→ Filtro por modalidade
→ Filtro por empresa
→ Filtro por cargo
→ Filtro por período
→ Pesquisa textual
→ Ordenação
```

### Dashboard

```text
→ Indicadores principais
→ Total de candidaturas
→ Entrevistas
→ Testes
→ Processos em andamento
→ Aprovadas
→ Recusadas
→ Indicadores por período
→ Gráficos
```

### Automação

```text
→ Atualização automática de dados
→ Organização automática
→ Detecção de duplicidades
→ Sugestões de empresas
→ Sugestões de cargos
→ Alertas
```

### IA

```text
→ Classificação de vagas
→ Extração de informações da vaga
→ Sugestão de cargo
→ Sugestão de empresa
→ Resumo da vaga
→ Comparação com perfil
→ Apoio à candidatura
```

### Deploy

```text
→ Preparação para produção
→ Configuração de variáveis de ambiente
→ Segurança
→ Banco em produção
→ Deploy
→ Domínio próprio
```

---

# 41. Roadmap visual

```text
                    JOB TRACKER
                         │
                         ▼
                 ┌───────────────┐
                 │     BASE      │
                 │ Django / DB   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │   USUÁRIOS    │
                 │ Login / Auth  │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ CANDIDATURAS  │
                 └───────┬───────┘
                         │
                         ▼
             ┌────────────────────────┐
             │ EMPRESAS + CARGOS      │
             │ Catálogo / Normalização│
             │ Aliases / Duplicidade  │
             └───────────┬────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      CRUD       │
                │ Editar/Excluir  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     FILTROS     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    DASHBOARD    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   AUTOMAÇÃO     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │       IA        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     DEPLOY      │
                └─────────────────┘
```

---

# 42. Regra de estudo adotada no projeto

O Job Tracker não está sendo desenvolvido apenas para terminar a aplicação.

Ele também está sendo utilizado como projeto de aprendizado.

A regra adotada é que cada mudança importante deve ser entendida, e não somente copiada.

Para cada alteração de código, devemos entender:

1. O que o código faz.
2. Por que ele é necessário.
3. O significado dos parâmetros.
4. Como uma parte conversa com outra.
5. O que aconteceria se aquela linha fosse removida.
6. Quais alternativas existem.

Por exemplo:

```css
font-size: 20px;
```

Não basta saber que aumenta o texto.

É importante entender:

* `font-size` controla o tamanho da fonte.
* `20px` é o valor escolhido.
* esse valor depende da hierarquia visual.
* títulos, subtítulos e textos auxiliares possuem funções diferentes.
* aumentar um elemento demais pode prejudicar a composição da página.

---

# 43. Evolução esperada do aprendizado

A intenção é migrar progressivamente de:

```text
"me dê o código"
```

para:

```text
"me explique para eu tentar"
```

e finalmente:

```text
"eu consigo construir sozinho"
```

Por isso, as próximas implementações devem continuar explicando:

```text
o que fazemos
        +
por que fazemos
        +
como funciona
        +
como poderíamos fazer diferente
```

---

# 44. Filosofia do projeto

O Job Tracker está sendo construído com duas metas simultâneas.

## Produto

Criar uma aplicação:

* funcional
* bonita
* organizada
* responsiva
* apresentável
* preparada para crescer

## Aprendizado

Utilizar o projeto para desenvolver conhecimento em:

* Python
* Django
* PostgreSQL
* Supabase
* modelagem de banco
* autenticação
* HTTP
* HTML
* CSS
* JavaScript futuramente
* Git
* GitHub
* testes
* automação
* IA
* deploy

---

# 45. Visão de arquitetura atual

```text
                         NAVEGADOR
                             │
                             ▼
                        Django URLs
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
               Landing                App
                                        │
                                        ▼
                                      Views
                                        │
                              ┌─────────┼─────────┐
                              ▼         ▼         ▼
                           Forms    Services    Auth
                              │         │
                              └────┬────┘
                                   ▼
                                 Models
                                   │
                                   ▼
                              PostgreSQL
                                   │
                                   ▼
                                Supabase
```

Com o crescimento do projeto, a arquitetura está caminhando para uma separação cada vez mais clara entre:

```text
Interface
    ↓
Views
    ↓
Regras de negócio
    ↓
Models
    ↓
Banco
```

---

# 46. Estado do projeto neste momento

O Job Tracker já ultrapassou a fase de:

```text
"site Django básico"
```

e entrou na fase de:

```text
"produto em evolução"
```

A fundação já está pronta.

A maior parte da estrutura necessária para empresas, cargos e candidaturas também já está implementada.

O próximo foco é transformar essa estrutura em uma experiência de uso mais completa:

```text
CRUD
   ↓
Filtros
   ↓
Dashboard
   ↓
Automação
   ↓
IA
   ↓
Deploy
```

---

## Observação

Esta documentação representa o estado conhecido do projeto após a evolução recente.

Ela deve ser atualizada sempre que uma mudança importante de arquitetura, banco de dados, interface ou funcionalidade for implementada.

O roadmap deve sempre refletir o estado real do sistema, evitando manter como "pendente" uma funcionalidade que já tenha sido concluída.
