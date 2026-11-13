# Matriz

## Matriz — Gestão de Projetos e Tarefas

Aplicação web para equipas organizarem projetos, tarefas, responsáveis e comentários. A arquitetura é um monólito modular Django/DRF com frontend React/Vite e PostgreSQL.

### Funcionalidades implementadas

- Autenticação por email e palavra-passe com sessões Django e proteção CSRF.
- Papéis Admin, Project Manager e Developer. O Admin pode consultar projetos e tarefas globalmente e gerir papéis de utilizadores existentes; não pode alterar projetos/tarefas nem adicionar comentários.
- Criação, consulta, atualização, eliminação e pesquisa de projetos.
- Gestão de membros por Project Manager; remover um membro também remove as suas atribuições no projeto.
- CRUD de tarefas com estados `TODO`, `IN_PROGRESS`, `DONE`, prioridades `LOW`, `MEDIUM`, `HIGH`, filtros e múltiplos responsáveis.
- Comentários com autor e data definidos pelo servidor.
- Painel inicial agregado no frontend a partir dos endpoints existentes; não há endpoints próprios para dashboard, progresso ou tarefas pessoais.

### Tecnologias e versões

| Componente | Versão/configuração observada |
|---|---|
| Python | 3.15.1 na imagem backend; execução local documentada para Python 3.12–3.15 |
| Django / Django REST Framework | 6.1.3 / 3.18.3 |
| PostgreSQL | 17 |
| Node.js | 22.23.4 na imagem frontend; local: 20.19+ (série 20) ou 22.12+ |
| React / Vite | 19.3.1 / 8.3.5 |
| Nginx | 1.29.3 |
| Playwright E2E | `@playwright/test` 1.56.1; imagem `v1.56.1-noble` |

As versões dos pacotes backend estão fixadas em `backend/requirements.txt`; as do frontend estão em `frontend/package-lock.json`.

### Pré-requisitos

- Git.
- Docker Engine e Docker Compose v2 para o caminho recomendado.
- Para execução sem Docker: Python 3.12–3.15, Node.js conforme acima, npm e PostgreSQL 17.
- Os comandos abaixo usam shell POSIX (macOS, Linux ou WSL2).

### Instalação recomendada (Docker Compose)

```sh
git clone https://github.com/simcampos/matriz---project-manager.git
cd matriz---project-manager
cp .env.example .env
```

Revê o `.env` antes de executar o seed. Define uma `DJANGO_SECRET_KEY` local, as credenciais de PostgreSQL (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`) e passwords locais para `DEMO_ADMIN_PASSWORD`, `DEMO_PM_PASSWORD` e `DEMO_DEVELOPER_PASSWORD`. Os valores do `.env.example` são apenas demonstração local; não os uses em produção nem os publiques.

Arranca a aplicação e aplica explicitamente migrations e seed:

```sh
docker compose up -d --build --wait
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo
```

A aplicação fica em <http://localhost:5174>, a API em <http://localhost:8001/api> e o health check em <http://localhost:8001/api/health/>. PostgreSQL fica em `localhost:5432`. Migrations e seed não correm automaticamente no arranque; o seed é idempotente.

O Compose local constrói o target `development` do backend, que usa o servidor de desenvolvimento Django.

### Execução sem Docker (desenvolvimento)

Instala PostgreSQL 17 e cria uma role e uma base de dados que correspondam às variáveis `POSTGRES_USER` e `POSTGRES_DB` do `.env`. Exemplo interativo em `psql` como administrador PostgreSQL:

```sh
psql -h localhost -U postgres
```

No prompt de `psql`:

```sql
CREATE ROLE matriz LOGIN;
CREATE DATABASE matriz OWNER matriz;
\password matriz
\q
```

Introduz no `.env` a mesma password definida para a role, `POSTGRES_HOST=127.0.0.1`, `POSTGRES_PORT=5432`, uma `DJANGO_SECRET_KEY` local e passwords para as contas de demonstração. Confirma também que `VITE_API_BASE_URL=http://localhost:8000/api` e que as origens CORS/CSRF incluem `http://localhost:5173`.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cd frontend && npm ci && cd ..
.venv/bin/python backend/manage.py migrate
.venv/bin/python backend/manage.py seed_demo
```

Arranca backend e frontend em terminais separados, a partir da raiz:

```sh
.venv/bin/python backend/manage.py runserver 127.0.0.1:8000
```

```sh
cd frontend && npm run dev
```

Abre <http://localhost:5173>. Esta configuração manual lê as variáveis do `.env` na raiz.

### Contas de demonstração

O seed cria contas fictícias; as passwords são definidas no `.env` e não são documentadas aqui.

| Email | Papel | Variável da password |
|---|---|---|
| `admin@matriz.dev` | Admin | `DEMO_ADMIN_PASSWORD` |
| `pm@matriz.dev` | Project Manager | `DEMO_PM_PASSWORD` |
| `developer@matriz.dev` | Developer | `DEMO_DEVELOPER_PASSWORD` |

### Testes

A partir da raiz:

```sh
.venv/bin/python backend/manage.py check
.venv/bin/python backend/manage.py test config.tests apps.accounts apps.projects apps.tasks apps.comments
cd frontend && npm test && npm run build
```

O E2E usa uma base PostgreSQL isolada e Docker Compose. Define no `.env` as variáveis `DJANGO_SECRET_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD` e as três `DEMO_*` antes de executar:

```sh
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e up -d --build --wait e2e-db e2e-backend e2e-frontend
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-setup migrate
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-setup seed_demo
docker compose -f compose.yaml -f compose.e2e.yaml --profile e2e run --rm e2e-runner
```

### CI e publicação de imagens

[`.github/workflows/ci.yml`](./.github/workflows/ci.yml) corre os testes backend e frontend em pushes para `main`/`develop` e pull requests para `main`; o job `build` depende do sucesso de `test` e verifica a imagem da API com o target `production`. [`.github/workflows/release.yml`](./.github/workflows/release.yml) constrói e publica as imagens da API e do frontend no GHCR em tags `v*.*.*`, usando `GITHUB_TOKEN`. Isto publica imagens no registry; não configura deployment da aplicação.

A imagem da API publicada usa o target `production` do [Dockerfile backend](./backend/Dockerfile), servido por Gunicorn e executado como utilizador não-root. Para executar esse target, configura no ambiente de runtime `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `DJANGO_CORS_ALLOWED_ORIGINS` e `DJANGO_CSRF_TRUSTED_ORIGINS`; mantém `DJANGO_DEBUG=false` (o default da imagem). Não uses os valores de demonstração de `.env.example` em produção. A imagem não aplica migrations nem executa o seed: aplica migrations como operação explícita de release e não executes `seed_demo` em produção. Hosting, TLS e deployment continuam por configurar.

### Deployment de protótipo no Render

[`render.yaml`](./render.yaml) define a API Django, o frontend Nginx e PostgreSQL em Frankfurt, usando planos gratuitos para prototipagem. O frontend encaminha `/api/` para a API e serve a aplicação e os cookies de sessão na mesma origem, preservando a autenticação e CSRF existentes. Os serviços têm o auto-deploy do Render desligado: o job `deploy` em [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) pede ao Render o deploy do SHA exato apenas depois de passarem os testes e o build, em pushes para `main`.

Antes do primeiro deploy:

1. Confirma que o último commit de `main` passou na CI. No Render, cria um Blueprint a partir deste repositório e revê os serviços e os domínios antes de aplicar. O primeiro Apply inicia os serviços; os deploys seguintes são acionados pela CI.
2. O job de deploy da CI é ignorado até existirem os dois IDs dos serviços; assim, o primeiro merge pode executar testes e build sem falhar por falta da configuração do Render. O primeiro Apply do Blueprint inicia o deploy inicial.
3. No GitHub, cria o Environment `production`. Adiciona `RENDER_API_KEY` como **Environment secret** e `RENDER_API_SERVICE_ID` e `RENDER_FRONTEND_SERVICE_ID` como **Environment variables**. Obtém os IDs no Dashboard do Render. Nunca coloques a chave de API em `.env`, no repositório ou nesta conversa. Depois de definidos os IDs, os pushes seguintes para `main` fazem deploy após a CI.
4. Confirma que o domínio do frontend corresponde a `matriz-project-manager-web.onrender.com`; se o Render atribuir outro, atualiza `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS` em `render.yaml` antes de sincronizar o Blueprint.
5. A base de dados é criada com acesso externo bloqueado. Para aplicar as migrations iniciais no plano gratuito, adiciona temporariamente à allow list da base de dados apenas o IP de confiança usado para a operação, coloca a connection string externa em `DATABASE_URL` no `.env` local e executa `.venv/bin/python backend/manage.py migrate`. Remove a regra de IP temporária no fim. Não executes `seed_demo` em produção.

Os planos gratuitos são apenas para protótipos: os serviços web podem adormecer após inatividade e a base de dados PostgreSQL gratuita expira ao fim de 30 dias. Nesse perfil, migrations não correm automaticamente; aplica-as explicitamente antes de releases que alterem o schema. Para migrations automáticas com `preDeployCommand`, usa um plano pago de serviço web. O Render CLI não é necessário para a pipeline, mas antes de aplicar podes validar o Blueprint com `render blueprints validate render.yaml`.

### Documentação e contrato

- [Requisitos](./docs/requirements.md), [User Stories](./docs/user-stories.md) e [Restrições](./docs/constraints.md).
- [Arquitetura](./docs/architecture.md), [modelo de dados](./docs/database.md), [plano de implementação](./docs/implementation-plan.md) e [verificação registada](./docs/verification.md).
- [OpenAPI 3.1](./openapi.yaml).
- [CHANGELOG](./CHANGELOG.md) e [notas da versão candidata](./docs/release-notes-v0.1.0-rc.4.md).
