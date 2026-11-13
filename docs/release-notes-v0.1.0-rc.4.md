# Matriz v0.1.0-rc.4 — Notas de versão candidata

**Estado:** proposta para revisão; não publicada. A tag não foi criada.

A tag `v0.1.0-rc.1` já existe (assim como `rc.2` e `rc.3`), pelo que a próxima candidata sugerida é `v0.1.0-rc.4`. Não apagar nem substituir tags existentes.

## Incluído

- Login/logout com sessão Django e CSRF.
- Gestão de projetos, pesquisa, membros e permissões por papel.
- Gestão de tarefas, estados, prioridades, filtros e responsáveis múltiplos.
- Comentários e painel inicial agregado no frontend.
- Docker Compose local e E2E; CI com testes e build Docker; workflow de publicação GHCR por tag.
- OpenAPI 3.1 para as rotas REST, com `info.version` alinhado a `0.1.0-rc.4`.

## Instalação resumida

```sh
git clone https://github.com/simcampos/matriz---project-manager.git
cd matriz---project-manager
cp .env.example .env
# Rever no .env DJANGO_SECRET_KEY, POSTGRES_* e DEMO_* para uso local
docker compose up -d --build --wait
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo
```

Frontend: <http://localhost:5174>; API: <http://localhost:8001/api>.

## Limitações e questões por confirmar

- Não há endpoints REST próprios para dashboard, progresso do projeto ou lista de tarefas pessoais; o frontend agrega dados das rotas existentes.
- Listagens sem paginação.
- O Compose usa Django `runserver` e é apenas para desenvolvimento/validação, não produção.
- A imagem frontend usa `VITE_API_BASE_URL` em build; não existe configuração de deployment/URL pública da API.
- Criação/convite/desativação de utilizadores, duração de sessão, privacidade/retenção e requisitos mensuráveis de produção continuam por definir.

## Próximos passos

1. Rever estes documentos e confirmar os limites de produto ainda pendentes.
2. Validar o quickstart a partir de um clone limpo e executar testes backend, frontend e E2E.
3. Definir deployment e configuração de produção antes de qualquer release de produção.
4. Após aprovação, escolher o commit de release e criar a tag candidata. Não executar estes comandos nesta tarefa:

```sh
git tag -a v0.1.0-rc.4 -m "Release candidate 4 — MVP Matriz"
git push origin v0.1.0-rc.4
```
