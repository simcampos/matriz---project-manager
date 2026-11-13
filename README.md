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

## Execução local com Docker Compose

O Compose arranca PostgreSQL, a API Django e o frontend estático gerado pelo Vite e servido por Nginx. Este perfil é para validação local; não é a configuração de produção do Render. O backend usa Django `runserver`, enquanto o perfil E2E mantém os seus serviços isolados.

É necessário Docker Engine com Docker Compose v2. Não é necessário instalar Python nem Node.js no host para executar esta opção:

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo
```

O seed é opcional e as migrations/seed são sempre comandos explícitos; o arranque dos containers não altera dados. Define as passwords de demonstração no `.env` antes de executar o seed.

A aplicação fica disponível em `http://localhost:5174`; a API pode ser verificada em `http://localhost:8001/api/health/`. O frontend comunica diretamente com a API publicada em `http://localhost:8001/api`, com as origens CORS/CSRF limitadas ao frontend local. Os serviços partilham a rede Compose `matriz`; a base de dados também fica disponível no host em `localhost:5432`. Os dados persistem no volume `postgres_data`.

Se o Docker estiver numa rede com inspeção TLS e o npm não confiar na CA instalada no host, segue os passos de certificado PEM da secção E2E, define `E2E_CA_CERT_PATH` para o ficheiro PEM e acrescenta `-f compose.dev.ca.yaml` ao comando Compose. O override disponibiliza a CA apenas como BuildKit secret durante a instalação npm; não a copia para a imagem.

O frontend é compilado durante o build da imagem. Para incluir alterações ao código:

```sh
docker compose up -d --build --wait
```

O frontend usa Nginx para servir os ficheiros estáticos compilados; o backend continua a executar Django `runserver`, pelo que este Compose não é uma configuração de produção. O deployment no Render permanece para uma fase posterior. O workflow [release.yml](./.github/workflows/release.yml) publica as imagens da API e do frontend no GHCR ao enviar tags `v*.*.*`, usando `GITHUB_TOKEN`. A imagem do frontend mantém o valor predefinido `VITE_API_BASE_URL=http://localhost:8000/api`.

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

Na execução manual, o backend e o Vite leem a configuração do `.env` na raiz. `VITE_API_BASE_URL` é o endereço centralizado da API; o valor de exemplo aponta para `http://localhost:8000/api`. No Compose, o endereço `http://localhost:8001/api` é definido como argumento de build do frontend. Para alterar as origens da execução manual, atualiza também as origens CORS/CSRF correspondentes no `.env`.

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

No início do trabalho, verificar os serviços Compose antes de os arrancar. O health check da API confirma também a ligação à base de dados:

```sh
docker compose ps db backend frontend
curl --fail --silent --show-error http://localhost:8001/api/health/
curl --fail --silent --show-error --output /dev/null --write-out 'HTTP %{http_code}\n' http://localhost:5174/
```

Se a base de dados não estiver ativa, arrancá-la e esperar que fique pronta:

```sh
docker compose up -d --wait db
```

Se o backend ou frontend não responder, arrancar apenas o serviço em falta com `docker compose up -d --build --wait backend` ou `docker compose up -d --build --wait frontend`. Não parar os serviços no fim do trabalho. O arranque não executa migrations nem seed e não altera dados.

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

O backend manual fica disponível em `http://localhost:8000` e o frontend em `http://localhost:5173`.

## Testes e verificações

Executar a partir da raiz do repositório:

```sh
.venv/bin/python backend/manage.py check
.venv/bin/python backend/manage.py test apps.accounts apps.projects apps.tasks apps.comments
cd frontend
npm test
npm run build
```

O workflow [ci.yml](./.github/workflows/ci.yml) executa os testes backend e frontend em pushes para `main`/`develop` e em pull requests para `main`; só constrói as imagens Docker se todos os testes passarem.

O seed pode ser executado novamente sem duplicar os registos de demonstração. Os resultados das verificações funcionais e as limitações conhecidas estão em [verification.md](./docs/verification.md).

O modelo lógico e as escolhas de persistência estão descritos em [database.md](./docs/database.md). Os estados são `TODO`, `IN_PROGRESS` e `DONE`; prioridades são `LOW`, `MEDIUM` e `HIGH`, com defaults `TODO` e `MEDIUM`. As sessões são geridas por Django; a tabela `django_session` é criada pelas migrations do framework.

### Teste E2E com Playwright

O fluxo E2E testa login de Project Manager, abertura do painel e criação de um projeto e de uma tarefa pela interface. O runner Playwright/Chromium, frontend, backend e PostgreSQL E2E correm em containers numa rede Compose isolada. O código do frontend e backend é bind-mounted do repositório no host, por isso as alterações feitas no VS Code ficam visíveis nos containers sem reconstruir imagens. `node_modules` fica num volume Docker separado das dependências instaladas no host.

O serviço `e2e-db` usa a base `matriz_e2e` e um volume próprios; não usa a base de desenvolvimento `matriz`. Migrations e seed são comandos explícitos e nunca são executados automaticamente ao arrancar os serviços. O `.env` é lido pelo Compose em runtime; não é copiado para as imagens. Define nele `DJANGO_SECRET_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD` e as três passwords `DEMO_*`.

```sh
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e up -d --build --wait e2e-db e2e-backend e2e-frontend
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-setup migrate
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-setup seed_demo
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-runner
```

O runner usa a imagem oficial Playwright `v1.56.1-noble`, alinhada com a versão de `@playwright/test` no lockfile, e não requer Chromium instalado no host. O frontend usa o Vite como proxy de `/api` para o backend, mantendo os pedidos e cookies da sessão na mesma origem. O teste usa `pm@matriz.dev`; para outra conta já existente na base E2E, define `E2E_PM_EMAIL` no `.env`.

As dependências do frontend são instaladas no volume `e2e_node_modules` na primeira execução e reinstaladas quando `package.json` ou `package-lock.json` mudam. Assim, recriar o container frontend para correr o runner não exige acesso repetido ao npm.

Se o Docker usar uma rede com inspeção TLS e o npm não confiar na CA instalada no host, exporta a CA confiável para um ficheiro PEM local e adiciona `-f compose.e2e.ca.yaml` a cada comando Compose E2E. No macOS, por exemplo:

```sh
security find-certificate -a -p > /tmp/matriz-e2e-ca.pem
export E2E_CA_CERT_PATH=/tmp/matriz-e2e-ca.pem
```

O ficheiro PEM é montado apenas nos containers frontend e runner e não deve ser versionado.

Os resultados HTML ficam em `frontend/playwright-report/`; screenshots e traces só são guardados em falhas, em `frontend/test-results/`. Estes ficheiros aparecem no repositório do host através do bind mount. A base E2E permanece no volume entre execuções; o seed é idempotente e não altera passwords de contas já existentes.

Para parar manualmente apenas os serviços E2E quando já não forem necessários:

```sh
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e stop e2e-backend e2e-frontend e2e-db
```

#### Alternativa: runner local

Também é possível executar o runner no host. Esta opção requer Chromium do Playwright instalado localmente ou um executável Chromium/Chrome indicado em `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. O backend e frontend são iniciados pelo `webServer` do Playwright:

```sh
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e up -d --wait e2e-db
POSTGRES_DB=matriz_e2e POSTGRES_PORT=5433 .venv/bin/python backend/manage.py migrate
POSTGRES_DB=matriz_e2e POSTGRES_PORT=5433 .venv/bin/python backend/manage.py seed_demo
cd frontend
npm run test:e2e
```
