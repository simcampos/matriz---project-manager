# Changelog

Registo de alterações relevantes do Matriz, seguindo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). As versões seguem Semantic Versioning. Esta entrada prepara uma release candidate; não significa que a release ou tag tenha sido publicada.

## [0.1.0-rc.4] - 2026-11-13

> Candidata preparada para revisão. Tag não criada; release não publicada.

### Added

- Aplicação web React/Vite e API Django REST para autenticação por sessão, projetos, membros, tarefas, responsáveis e comentários.
- Papéis Admin, Project Manager e Developer, filtros de tarefa e painel agregado no frontend.
- Execução local e E2E com Docker Compose.
- CI GitHub Actions para testes backend/frontend e build Docker condicionado ao sucesso dos testes.
- Publicação das imagens API/frontend no GHCR em tags de release, via `GITHUB_TOKEN`.
- Contrato da API em OpenAPI 3.1.

### Changed

- Validação de escrita partilhada para rejeitar campos desconhecidos.
- Admin limitado a leitura global de projetos/tarefas/comentários; gestão de papéis e membros protegida pelas regras implementadas.
- Composição local documentada com serviços PostgreSQL, backend e frontend e health checks.
- Versão `info.version` do OpenAPI alinhada com o candidato `0.1.0-rc.4`.

### Fixed

- Consulta inicial de sessão anónima deixa de ser tratada como sessão expirada; pedidos protegidos continuam a emitir o evento de expiração.
