# Plano de implementação — estado real

Este registo distingue funcionalidades presentes no repositório de operações ainda descritas nos requisitos ou em versões anteriores do contrato.

## Incrementos concluídos

| Incremento | Estado | Implementação |
|---|---|---|
| Autenticação e sessão | Concluído | Sessão Django, proteção CSRF, utilizador atual e logout. |
| Projetos | Concluído | CRUD, pesquisa por nome e controlo de acesso por projeto. A consulta de membros existe; a API não altera a composição do projeto. |
| Tarefas | Concluído | CRUD, estados, prioridades e filtros. As listas são completas e não paginadas. |
| Responsáveis e comentários | Concluído | Associar/remover responsáveis elegíveis; criar/listar comentários com autor e data atribuídos no backend. |
| Ecrãs do MVP | Concluído | Frontend integrado com as rotas reais; o painel agrega projetos/tarefas e calcula contagens no browser. |
| Refatoração de validação | Concluído | `StrictSerializer` centralizado em `backend/apps/common/serializers.py`; os testes backend e frontend e o build foram executados após a alteração. |
| Verificação funcional | Concluído | Os resultados manuais e automatizados estão registados em [verification.md](./verification.md). |

## Pendências reconhecidas

| Requisito ou operação | Estado real |
|---|---|
| RF-03 — gerir papéis de utilizadores pela aplicação | Pendente; não existe endpoint REST/UI de gestão de papéis. |
| RF-05 — adicionar/remover membros de projeto pela aplicação | Pendente; existe apenas consulta de membros. |
| Listar tarefas pessoais por endpoint próprio | Não implementado; não existe `GET /users/me/tasks/`. |
| Endpoint de progresso do projeto e endpoint de dashboard | Não implementados; as contagens do painel são calculadas no frontend a partir dos endpoints de projetos e tarefas. |
| Paginação | Não implementada; as rotas de listagem devolvem os resultados completos. |

As pendências de RF-03 e RF-05 foram mantidas de forma intencional e não devem ser tratadas como funcionalidades entregues. A preparação documental da entrega continua em curso até estarem concluídos o README reproduzível, os exemplos de uso de IA e a simulação de setup limpo.
