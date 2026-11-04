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
- Perfis propostos: Admin, Project Manager e Developer.
- CRUD e pesquisa de projetos por nome.
- CRUD de tarefas com estado e prioridade.
- Associação de membros a projetos e associação/remoção de vários responsáveis por tarefa.
- Comentários com autor e data.
- Estados de tarefa propostos e fixos.
- Filtros de tarefas por estado e prioridade.
- Painel inicial com projetos acessíveis e contagens de tarefas por estado.
- Consulta das tarefas atribuídas ao utilizador autenticado.

As funcionalidades acima refletem a ficha desta fase. A stack, as sessões Django, os códigos/defaults de estado e prioridade e a eliminação em cascata estão confirmados para a estrutura inicial. As regras de acesso por papel e detalhes dos comentários continuam propostas ou pendentes de validação. A escala de até cerca de 50 utilizadores é uma referência inicial, não um limite confirmado.

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
- [Wireframe do dashboard](./docs/ui/wireframe.png)

## Estado atual

A aplicação contém a estrutura inicial do backend e frontend, migrations reproduzíveis e seed de demonstração idempotente. O seed cria `admin@matriz.dev`, `pm@matriz.dev` e `developer@matriz.dev`, com passwords hasheadas. Os valores e credenciais de `.env.example` são apenas para desenvolvimento local; não reutilizar em produção.

## Desenvolvimento local

Na raiz do projeto:

```sh
cp .env.example .env
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cd frontend && npm ci && cd ..
docker compose up -d db
.venv/bin/python backend/manage.py migrate
.venv/bin/python backend/manage.py seed_demo
```

Arrancar o backend e o frontend em terminais separados:

```sh
DJANGO_SETTINGS_MODULE=config.settings .venv/bin/python backend/manage.py runserver
```

```sh
cd frontend && npm run dev
```

Para validar a instalação, executar `.venv/bin/python backend/manage.py test apps.accounts apps.projects apps.tasks apps.comments` e `cd frontend && npm run build`. O seed pode ser executado novamente sem apagar ou duplicar os dados existentes.

O modelo lógico e as escolhas de persistência estão descritos em [database.md](./docs/database.md). Os estados são `TODO`, `IN_PROGRESS` e `DONE`; prioridades são `LOW`, `MEDIUM` e `HIGH`, com defaults `TODO` e `MEDIUM`. As sessões são geridas por Django; a tabela `django_session` é criada pelas migrations do framework.
