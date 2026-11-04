# Requisitos — Matriz

## Visão e objetivos da aplicação

O Matriz é uma aplicação web de gestão de projetos e tarefas para equipas. Pretende ajudar as equipas a organizar projetos, gerir e atribuir trabalho e acompanhar o progresso das tarefas.

O objetivo do MVP é disponibilizar um fluxo simples que permita autenticar utilizadores, organizar projetos, gerir tarefas, atribuir responsáveis e consultar o progresso. O âmbito desta fase inclui também prioridade, comentários, pesquisa de projetos e um painel inicial, conforme a ficha de implementação. As regras de negócio que a ficha não fixa continuam identificadas como propostas ou decisões pendentes.

### Factos e pressupostos de contexto

**Factos explicitamente comunicados pelo cliente**

- O cliente precisa de uma aplicação para as suas equipas.
- As equipas devem poder organizar projetos, gerir tarefas e acompanhar o progresso do trabalho.

**Pressupostos fornecidos para definir o MVP**

- Os perfis considerados são Admin, Project Manager e Developer.
- A escala de referência é uma equipa pequena/média, até cerca de 50 utilizadores; não é um limite funcional confirmado.
- O acesso será feito através de um browser web.
- A autenticação será por email e palavra-passe.
- Não haverá integrações externas no MVP.

**Escolhas confirmadas para a estrutura inicial**

- Backend Python com Django/DRF; frontend React/Vite; PostgreSQL com Django ORM.
- Autenticação por sessões server-side Django.
- Estados `TODO`, `IN_PROGRESS`, `DONE`; prioridades `LOW`, `MEDIUM`, `HIGH`, com defaults `TODO` e `MEDIUM`.
- Eliminação em cascata de dados dependentes de projetos e tarefas.

### Terminologia

Neste documento, **Admin**, **Project Manager** e **Developer** são os nomes provisórios dos três papéis. “Palavra-passe” designa a credencial de autenticação. Os nomes dos papéis e as responsabilidades ainda precisam de validação pelo cliente.

## Tipos de utilizadores

| Tipo | Responsabilidades propostas |
|---|---|
| **Admin** | Consultar utilizadores existentes e atribuir papéis; o alcance do acesso administrativo a projetos ainda não está definido. |
| **Project Manager** | Criar e gerir projetos, organizar tarefas, atribuir responsáveis e acompanhar o progresso. |
| **Developer** | Consultar projetos a que tem acesso e atualizar o estado das tarefas que lhe estão atribuídas. |

As permissões exatas, o acesso administrativo e a possibilidade de acumular papéis ainda precisam de confirmação.

## Requisitos funcionais

Os requisitos abaixo descrevem o âmbito desta fase. A ficha de implementação define as funcionalidades; as regras de acesso, campos, valores e comportamentos não determinados por ela continuam propostas para validação.

| ID | Requisito | Prioridade |
|---|---|---|
| **RF-01** | O sistema deve permitir que um utilizador inicie e termine sessão usando email e palavra-passe. | Alta |
| **RF-02** | O sistema deve distinguir os papéis Admin, Project Manager e Developer e limitar as ações de acordo com as permissões definidas. | Alta |
| **RF-03** | O Admin deve poder consultar os utilizadores da equipa e atribuir a utilizadores existentes um dos papéis disponíveis. | Alta |
| **RF-04** | O Project Manager deve poder criar, consultar, atualizar e eliminar projetos a que tem acesso de gestão. A proposta para validação é exigir título e permitir descrição opcional. A implementação atual valida títulos entre 3 e 100 caracteres e descrições até 1000 caracteres; estes limites ainda carecem de confirmação do cliente. | Alta |
| **RF-05** | O Project Manager deve poder associar membros existentes aos projetos que gere. Um utilizador não associado não deve poder consultar nem alterar o projeto ou as suas tarefas. O Project Manager responsável conta implicitamente como membro do projeto. | Alta |
| **RF-06** | O Project Manager deve poder criar, consultar, atualizar e eliminar tarefas associadas a um projeto. O título é obrigatório, tem entre 3 e 150 caracteres e não pode conter apenas espaços; a descrição é opcional e limitada a 2000 caracteres. As tarefas aceitam os estados `TODO`, `IN_PROGRESS`, `DONE` e prioridades `LOW`, `MEDIUM`, `HIGH`; os defaults são `TODO` e `MEDIUM`. | Alta |
| **RF-07** | O sistema deve disponibilizar estados fixos `TODO`, `IN_PROGRESS` e `DONE`, apresentados como “Por fazer”, “Em progresso” e “Concluída”. | Alta |
| **RF-08** | O Project Manager deve poder associar e remover responsáveis de uma tarefa. Só utilizadores ativos que sejam membros do projeto ou o seu gestor são elegíveis; uma associação duplicada é recusada com conflito. A lista pode ficar vazia. | Alta |
| **RF-09** | O Developer deve poder atualizar o estado das tarefas que lhe estão atribuídas e a que tem acesso. O Project Manager deve poder atualizar tarefas dos projetos que gere. | Alta |
| **RF-10** | O sistema deve apresentar as tarefas de um projeto numa lista, com filtragem por estado e prioridade; o filtro por responsável do MVP anterior pode manter-se. | Alta |
| **RF-11** | O sistema deve apresentar, por projeto, a contagem de tarefas por estado e a lista de tarefas em aberto. A proposta é definir tarefas em aberto como tarefas em estado diferente de `DONE`; a visibilidade do resumo segue as regras de acesso a validar. | Alta |
| **RF-12** | O sistema deve permitir que o utilizador autenticado consulte as tarefas que lhe estão atribuídas em todos os projetos a que tem acesso, com filtragem opcional por estado e prioridade. | Média |
| **RF-13** | O sistema deve permitir pesquisar projetos pelo nome, limitando os resultados aos projetos acessíveis ao utilizador autenticado. | Alta |
| **RF-14** | Utilizadores com acesso ao projeto podem adicionar e listar comentários numa tarefa. O conteúdo é obrigatório, tem entre 1 e 2000 caracteres e não pode ser apenas espaços; o backend define autor e data, e a lista é cronológica (mais antigos primeiro). | Alta |
| **RF-15** | O painel inicial deve apresentar os projetos acessíveis ao utilizador e as contagens de tarefas por estado em cada projeto. | Alta |

Os critérios de aceitação detalhados estão em [user-stories.md](./user-stories.md).

## Stack e persistência aprovadas para a implementação inicial

- Backend: Python, Django e Django REST Framework.
- Frontend: React com Vite.
- Base de dados e ORM: PostgreSQL e Django ORM.
- Autenticação: password hashing e sessões server-side do Django; os dados de sessão são geridos pelo framework na tabela `django_session`.
- Valores persistidos de estado: `TODO`, `IN_PROGRESS`, `DONE`; de prioridade: `LOW`, `MEDIUM`, `HIGH`. Defaults: `TODO` e `MEDIUM`. A API usa cookies de sessão e proteção CSRF.

## Requisitos não funcionais

Os seguintes pontos são pressupostos ou propostas a validar, não compromissos de desempenho ou níveis de serviço:

- **Acesso:** a aplicação será utilizada através de um browser web.
- **Escala de referência:** equipa pequena/média, até cerca de 50 utilizadores; não é um limite funcional confirmado.
- **Autenticação:** o acesso será feito por email e palavra-passe.
- **Integrações:** não estão previstas integrações externas no MVP.
- **Segurança e privacidade:** as regras de acesso propostas devem impedir consulta e alteração por utilizadores não autorizados. Requisitos detalhados ainda precisam de aprovação.

Não foram definidos requisitos mensuráveis de disponibilidade, desempenho, acessibilidade, compatibilidade entre browsers, recuperação de desastres, retenção ou eliminação de dados. Estes devem ser acordados antes de se considerar o conjunto de requisitos fechado.

### Segurança e privacidade a validar

Como critérios propostos para revisão do cliente, o sistema deverá negar acesso a recursos sem autorização, evitar revelar se um email está registado em mensagens de autenticação e proteger credenciais e sessões. Os mecanismos, políticas de palavra-passe, recuperação de conta, expiração de sessão e prevenção de tentativas abusivas ainda não foram definidos.

Antes de produção, confirmar os dados pessoais tratados, respetiva finalidade, acesso permitido, retenção e eliminação, bem como requisitos aplicáveis de auditoria e recuperação de conta. Estes pontos não especificam tecnologias.

## Âmbito do MVP

O MVP inclui:

- Autenticação por email e palavra-passe.
- Gestão básica de utilizadores e dos três papéis definidos.
- Criação, consulta e atualização de projetos.
- Eliminação de projetos.
- Associação de membros a projetos e controlo de acesso proposto por projeto.
- Pesquisa de projetos por nome.
- Criação, consulta, atualização e eliminação de tarefas dentro de projetos, incluindo estado e prioridade.
- Associação e remoção de vários responsáveis por tarefa.
- Adição e listagem de comentários com autor e data.
- Estados de tarefa fixos.
- Atualização de estado pelo Developer para tarefas que lhe estão atribuídas e gestão de tarefas pelo Project Manager nos seus projetos.
- Lista de tarefas com filtragem por estado e prioridade.
- Resumo do progresso do projeto através de contagens por estado e tarefas em aberto.
- Consulta das tarefas atribuídas ao utilizador autenticado.
- Painel inicial com projetos acessíveis e contagens de tarefas por estado.

## Funcionalidades fora do âmbito inicial

As funcionalidades seguintes não fazem parte do MVP e só devem ser consideradas após validação:

- Integrações com serviços externos.
- Notificações e menções.
- Anexos em tarefas.
- Fluxos de trabalho, estados personalizados ou campos personalizados.
- Relatórios históricos, gráficos ou análise de tendências.
- Vistas adicionais, como quadro visual ou calendário.
- Subtarefas, dependências e marcos.
- Automações e importação de dados.
- Múltiplas equipas, permissões granulares e administração avançada.
- Arquivamento de projetos, até confirmação da necessidade e das regras de acesso após arquivo.

## Pontos a confirmar

- Confirmar os campos obrigatórios e os limites de tamanho: a proposta atual exige título e permite descrição opcional para projetos; a implementação valida título entre 3 e 100 caracteres e descrição até 1000 caracteres, ainda por confirmar com o cliente. Para tarefas exige título e estado e permite descrição opcional.
- Confirmar se prioridade deve poder ser alterada para além dos defaults aprovados.
- Confirmar se uma tarefa pode ficar sem responsáveis e se os responsáveis têm de ser membros do projeto.
- Estados de tarefa e transições permitidas.
- Regras de papéis, permissões, alcance do Admin, associação a projetos e atribuição de tarefas.
- A eliminação em cascata remove dados dependentes de projetos e tarefas; a interface deve tornar a consequência explícita.
- Definir o conteúdo permitido nos comentários, ordem da listagem e possibilidade de edição ou remoção (fora das operações mínimas pedidas).
- Validar que tarefas em aberto são as que não estão “Concluídas” e se o progresso deve incluir percentagens.
- Requisitos mínimos e mensuráveis de segurança, privacidade, disponibilidade e desempenho.
- Como criar, convidar, desativar e remover utilizadores; o MVP atual só descreve a gestão de papéis para utilizadores existentes.
- Como tratar atualizações concorrentes e falhas de gravação.
- Validar as decisões adotadas na Ficha PL 02: gestor único por projeto que conta implicitamente como membro, recusa de alterar o papel de quem gere projetos, resumo de progresso visível a qualquer utilizador com acesso ao projeto, sessão invalidada no servidor ao terminar sessão e vista das tarefas atribuídas ao utilizador (RF-12).
