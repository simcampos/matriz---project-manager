# Plano de implementação — estado real

Este registo distingue funcionalidades presentes no repositório de operações ainda descritas nos requisitos ou em versões anteriores do contrato.

## Incrementos concluídos

| Incremento | Estado | Implementação |
|---|---|---|
| Autenticação e sessão | Concluído | Sessão Django, proteção CSRF, utilizador atual e logout. |
| Projetos e membros | Concluído | CRUD, pesquisa, controlo de acesso, consulta/associação/remoção de membros; a remoção limpa as atribuições do membro no projeto. |
| Tarefas | Concluído | CRUD, estados, prioridades e filtros. As listas são completas e não paginadas. |
| Responsáveis e comentários | Concluído | Associar/remover responsáveis elegíveis; criar/listar comentários com autor e data atribuídos no backend. |
| Administração de utilizadores | Concluído | Admin lista utilizadores e altera papéis; a API impede ficar sem Admin ativo e protege gestores de projetos contra rebaixamento. |
| Leitura global Admin | Concluído | Admin consulta todos os projetos e dados das tarefas sem permissões de alteração nem de adicionar comentários. |
| Ecrãs do MVP | Concluído | Frontend integrado com as rotas reais; o painel agrega projetos/tarefas e calcula contagens no browser. |
| Refatoração de validação | Concluído | `StrictSerializer` centralizado em `backend/apps/common/serializers.py`; os testes backend e frontend e o build foram executados após a alteração. |
| Verificação funcional | Concluído | Os resultados manuais e automatizados estão registados em [verification.md](./verification.md). |

## Pendências reconhecidas

| Requisito ou operação | Estado real |
|---|---|
| Listar tarefas pessoais por endpoint próprio | Não implementado; não existe `GET /users/me/tasks/`. |
| Endpoint de progresso do projeto e endpoint de dashboard | Não implementados; as contagens do painel são calculadas no frontend a partir dos endpoints de projetos e tarefas. |
| Paginação | Não implementada; as rotas de listagem devolvem os resultados completos. |

RF-03 e RF-05 deixaram de estar pendentes. As limitações restantes são listagens sem paginação e ausência de endpoints dedicados para tarefas pessoais, progresso e painel. A cobertura de verificação atualizada está em [verification.md](./verification.md).
