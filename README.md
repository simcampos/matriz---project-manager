# Matriz

O **Matriz** é uma aplicação de gestão de projetos e tarefas para equipas. O projeto está na fase de definição e desenho: ainda não foram escolhidas tecnologias, mas já foram adotados o monólito modular como arquitetura e propostos o modelo de dados, o contrato de API e um wireframe.

## Problema e objetivos

O cliente identificou a necessidade de organizar projetos, gerir tarefas e acompanhar o progresso do trabalho. O Matriz pretende reunir estas atividades num único espaço.

Os principais objetivos são:

- Organizar o trabalho por projeto.
- Criar e gerir tarefas e respetivos responsáveis.
- Acompanhar o progresso através do estado das tarefas.
- Aplicar acesso adequado aos utilizadores.

## Âmbito proposto para o MVP

- Autenticação por email e palavra-passe.
- Perfis propostos: Admin, Project Manager e Developer.
- Gestão básica de projetos e tarefas.
- Associação de membros a projetos e atribuição de tarefas.
- Estados de tarefa propostos e fixos.
- Lista de tarefas e resumo do progresso por projeto.
- Consulta das tarefas atribuídas ao utilizador autenticado.

Este âmbito é uma proposta baseada em pressupostos, não uma especificação aprovada pelo cliente. A escala de até cerca de 50 utilizadores é uma referência inicial, não um limite confirmado.

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

O projeto está na fase de requisitos e desenho. Os artefactos de arquitetura, dados, API e interface são propostas em revisão; ainda não foi iniciada a implementação da aplicação.
