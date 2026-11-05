# Matriz

O **Matriz** é uma aplicação de gestão de projetos e tarefas para equipas. A estrutura inicial usa monólito modular com Python/Django e Django REST Framework, React/Vite, PostgreSQL e Django ORM.

## Problema e objetivos

O cliente identificou a necessidade de organizar projetos, gerir tarefas e acompanhar o progresso do trabalho. O Matriz pretende reunir estas atividades num único espaço.

Os principais objetivos são:

- Organizar o trabalho por projeto.
- Criar e gerir tarefas e respetivos responsáveis.
- Acompanhar o progresso através do estado das tarefas.
- Aplicar acesso adequado aos utilizadores.

## Âmbito desta fase

- Autenticação por email e palavra-passe.
- Papéis de utilizador: Admin, Project Manager e Developer.
- CRUD e pesquisa de projetos por nome.
- CRUD de tarefas com estado e prioridade.
- Gestão de membros de projeto pelo respetivo Project Manager e associação/remoção de vários responsáveis por tarefa.
- Administração: listar utilizadores e alterar papéis; o Admin pode consultar todos os projetos e tarefas, sem os alterar nem comentar.
- Comentários com autor e data.
- Estados de tarefa fixos.
- Filtros de tarefas por estado e prioridade.
- Painel inicial com projetos acessíveis, contagens por estado e tarefas atribuídas ao utilizador, calculados no frontend.

RF-03 (gestão de papéis) e RF-05 (associação/remoção de membros) estão implementados. Não existem endpoints REST próprios para tarefas pessoais, progresso ou painel; o frontend compõe o painel a partir das rotas implementadas. A descrição detalhada está em [implementation-plan.md](./docs/implementation-plan.md). As regras de acesso por papel e as decisões ainda pendentes estão registadas em [constraints.md](./docs/constraints.md).

## Documentação

- [Requisitos e âmbito do MVP](./docs/requirements.md)
- [User Stories e critérios de aceitação](./docs/user-stories.md)
- [Restrições, pressupostos e decisões pendentes](./docs/constraints.md)
- [Análise inicial de requisitos](./docs/analise-requisitos-iniciais.md)
- [Âmbito funcional do MVP](./docs/ambito-funcional-mvp.md)
- [Backlog inicial (redirecionamento)](./docs/backlog-inicial.md)
- [Arquitetura (monólito modular)](./docs/architecture.md)
- [Modelo de dados e diagrama ER](./docs/database.md)
- [Contrato da API (OpenAPI 3.1)](./openapi.yaml)
- [Estado real do plano de implementação](./docs/implementation-plan.md)
- [Registo de verificação](./docs/verification.md)
- [Wireframe do dashboard](./docs/ui/wireframe.png)

## Estado atual

A aplicação inclui migrations e um seed de demonstração idempotente. O seed cria `admin@matriz.dev`, `pm@matriz.dev` e `developer@matriz.dev`, projetos, tarefas, membros e atribuições. As passwords são lidas das variáveis `DEMO_ADMIN_PASSWORD`, `DEMO_PM_PASSWORD` e `DEMO_DEVELOPER_PASSWORD` do ficheiro local `.env`; define-as antes da primeira execução do seed. O seed não altera a password de contas que já existam. Os valores de `.env.example` destinam-se apenas a desenvolvimento local e não devem ser usados em produção.

## Pré-requisitos

- Python 3.12, 3.13, 3.14 ou 3.15 (Django 6.1.3; [compatibilidade oficial](https://docs.djangoproject.com/en/6.1/releases/6.1/)).
- Node.js 20.19 ou superior na série 20, ou 22.12 ou superior (requisito de Vite 8 no lockfile).
- npm compatível com a versão instalada do Node.js.
- Docker Engine com Docker Compose v2 ou mais recente e suporte a `up --wait` para arrancar a base de dados incluída; o [compose.yaml](./compose.yaml) usa PostgreSQL 17. Em alternativa, pode ser usado um servidor PostgreSQL 17 local.

## Instalação e configuração local

Executar a partir da raiz do repositório:

```sh
cp .env.example .env
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cd frontend && npm ci
cd ..
docker compose up -d --wait db
.venv/bin/python backend/manage.py migrate
.venv/bin/python backend/manage.py seed_demo
```

O backend e o Vite leem a configuração do `.env` na raiz. `VITE_API_BASE_URL` é o endereço centralizado da API; o valor de exemplo aponta para `http://localhost:8000/api`. Para usar outro endereço, atualiza essa variável e as origens CORS/CSRF correspondentes no `.env`.

O `.env` é local e não deve ser versionado; o ficheiro de referência versionado é `.env.example`.

O Compose mantém os dados da base de dados num volume Docker. Para usar PostgreSQL local em vez do serviço Compose, configura `POSTGRES_HOST` e `POSTGRES_PORT` no `.env` antes de executar migrations e seed.

### Contas de demonstração

| Email | Papel | Variável da password local |
|---|---|---|
| `admin@matriz.dev` | Admin | `DEMO_ADMIN_PASSWORD` |
| `pm@matriz.dev` | Project Manager | `DEMO_PM_PASSWORD` |
| `developer@matriz.dev` | Developer | `DEMO_DEVELOPER_PASSWORD` |

As passwords de demonstração são fictícias e locais. Consulta ou altera os respetivos valores no `.env`; não são repetidos neste documento. Altera-os antes de executar o seed pela primeira vez e não os reutilizes fora do ambiente local.

## Executar

### Verificar e reutilizar serviços em execução

No início do trabalho, verificar a base de dados e os serviços antes de os arrancar. O health check da API confirma também a ligação à base de dados:

```sh
docker compose ps db
curl --fail --silent --show-error http://localhost:8000/api/health/
curl --fail --silent --show-error --output /dev/null --write-out 'HTTP %{http_code}\n' http://localhost:5173/
```

Se a base de dados não estiver ativa, arrancá-la e esperar que fique pronta:

```sh
docker compose up -d --wait db
```

Se o backend ou frontend não responder, arrancar apenas o serviço em falta. Não parar os serviços no fim do trabalho. O arranque não executa migrations nem seed e não altera dados.

### Arranque manual

Quando necessário, iniciar o backend e o frontend em terminais separados, a partir da raiz do repositório:

```sh
cd backend
../.venv/bin/python manage.py runserver 127.0.0.1:8000
```

```sh
cd frontend
npm run dev
```

O backend fica disponível em `http://localhost:8000` e o frontend em `http://localhost:5173`.

## Testes e verificações

Executar a partir da raiz do repositório:

```sh
.venv/bin/python backend/manage.py check
.venv/bin/python backend/manage.py test apps.accounts apps.projects apps.tasks apps.comments
cd frontend
npm test
npm run build
```

O seed pode ser executado novamente sem duplicar os registos de demonstração. Os resultados das verificações funcionais e as limitações conhecidas estão em [verification.md](./docs/verification.md).

O modelo lógico e as escolhas de persistência estão descritos em [database.md](./docs/database.md). Os estados são `TODO`, `IN_PROGRESS` e `DONE`; prioridades são `LOW`, `MEDIUM` e `HIGH`, com defaults `TODO` e `MEDIUM`. As sessões são geridas por Django; a tabela `django_session` é criada pelas migrations do framework.

### Teste E2E com Playwright

O fluxo E2E testa login de Project Manager, abertura do painel e criação de um projeto e de uma tarefa pela interface. Usa um serviço PostgreSQL separado (`matriz_e2e`) numa porta/volume próprios; não aponta para a base de desenvolvimento `matriz`. O teste cria um projeto com nome único e tenta eliminá-lo no teardown, incluindo as tarefas dependentes.

Pré-requisitos: concluir a instalação local acima, ter `DEMO_PM_PASSWORD`, `POSTGRES_USER` e `POSTGRES_PASSWORD` definidos no `.env`, e instalar o browser Playwright:

```sh
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e up -d --wait e2e-db
POSTGRES_DB=matriz_e2e POSTGRES_PORT=5433 .venv/bin/python backend/manage.py migrate
POSTGRES_DB=matriz_e2e POSTGRES_PORT=5433 .venv/bin/python backend/manage.py seed_demo
cd frontend
npx playwright install chromium
npm run test:e2e
```

O comando E2E lê o `.env` da raiz para obter as credenciais de demonstração. Playwright inicia o backend e o frontend em `http://127.0.0.1:8001` e `http://127.0.0.1:5174`, respetivamente; esses processos são geridos pelo runner. O teste usa a conta `pm@matriz.dev` criada pelo seed, mas não depende dos projetos nem das tarefas seed. Para uma conta diferente, define `E2E_PM_EMAIL` no ambiente antes de executar.

Os resultados HTML ficam em `frontend/playwright-report/`; screenshots e traces só são guardados em falhas, em `frontend/test-results/`. A base `matriz_e2e` permanece no volume isolado entre execuções; as migrations e o seed devem ser executados apenas com `POSTGRES_DB=matriz_e2e` e `POSTGRES_PORT=5433`, como nos comandos acima.

Se já existir um Chromium/Chrome instalado e não for possível instalar o browser gerido pelo Playwright, pode indicar o executável ao runner com `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/caminho/para/chrome` antes de `npm run test:e2e`.
