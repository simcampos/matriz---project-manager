# Requisitos — Matriz

## Visão e objetivos da aplicação

O Matriz é uma aplicação web de gestão de projetos e tarefas para equipas. Pretende ajudar as equipas a organizar projetos, gerir e atribuir trabalho e acompanhar o progresso das tarefas.

O objetivo do MVP é disponibilizar um fluxo simples que permita autenticar utilizadores, organizar projetos, gerir tarefas, atribuir responsáveis e consultar o progresso de cada projeto. A visão e os requisitos aqui descritos baseiam-se na descrição inicial do cliente e em pressupostos fornecidos para a fase inicial; devem ser validados antes de serem tratados como requisitos finais.

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

Os requisitos abaixo descrevem o âmbito proposto para o MVP. A prioridade é Alta, salvo indicação diferente.

| ID | Requisito | Prioridade |
|---|---|---|
| **RF-01** | O sistema deve permitir que um utilizador inicie e termine sessão usando email e palavra-passe. | Alta |
| **RF-02** | O sistema deve distinguir os papéis Admin, Project Manager e Developer e limitar as ações de acordo com as permissões definidas. | Alta |
| **RF-03** | O Admin deve poder consultar os utilizadores da equipa e atribuir a utilizadores existentes um dos papéis disponíveis. | Alta |
| **RF-04** | O Project Manager deve poder criar, consultar e atualizar projetos. A proposta para validação é exigir título e permitir descrição opcional. | Alta |
| **RF-05** | O Project Manager deve poder associar membros existentes aos projetos que gere. Um utilizador não associado não deve poder consultar nem alterar o projeto ou as suas tarefas. | Alta |
| **RF-06** | O Project Manager deve poder criar, consultar e atualizar tarefas associadas a um projeto. A proposta para validação é exigir título e estado, permitir descrição opcional e permitir tarefa sem responsável. | Alta |
| **RF-07** | O sistema deve disponibilizar um conjunto fixo e comum de estados de tarefa. A proposta inicial é “Por fazer”, “Em progresso” e “Concluída”. | Alta |
| **RF-08** | O Project Manager deve poder atribuir uma tarefa a um membro associado ao projeto. | Alta |
| **RF-09** | O Developer deve poder atualizar o estado das tarefas que lhe estão atribuídas e a que tem acesso. O Project Manager deve poder atualizar tarefas dos projetos que gere. | Alta |
| **RF-10** | O sistema deve apresentar as tarefas de um projeto numa lista, com filtragem básica por estado e responsável. | Média |
| **RF-11** | O sistema deve apresentar, por projeto, a contagem de tarefas por estado e a lista de tarefas em aberto. Para esta proposta, “em aberto” significa estado diferente de “Concluída”. | Alta |

Os critérios de aceitação detalhados estão em [user-stories.md](./user-stories.md).

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
- Associação de membros a projetos e controlo de acesso proposto por projeto.
- Criação, consulta, atualização e atribuição de tarefas dentro de projetos.
- Estados de tarefa fixos.
- Atualização de estado pelo Developer para tarefas que lhe estão atribuídas e gestão de tarefas pelo Project Manager nos seus projetos.
- Lista de tarefas com filtragem básica por estado e responsável.
- Resumo do progresso do projeto através de contagens por estado e tarefas em aberto.

## Funcionalidades fora do âmbito inicial

As funcionalidades seguintes não fazem parte do MVP e só devem ser consideradas após validação:

- Integrações com serviços externos.
- Notificações, comentários e menções.
- Anexos em tarefas.
- Fluxos de trabalho, estados, prioridades ou campos personalizados.
- Relatórios históricos, gráficos ou análise de tendências.
- Vistas adicionais, como quadro visual ou calendário.
- Subtarefas, dependências e marcos.
- Automações e importação de dados.
- Múltiplas equipas, permissões granulares e administração avançada.
- Arquivamento de projetos, até confirmação da necessidade e das regras de acesso após arquivo.

## Pontos a confirmar

- Confirmar os campos obrigatórios: a proposta atual exige título e permite descrição opcional para projetos; para tarefas exige título e estado, permite descrição opcional e responsável opcional.
- Se a prioridade e o prazo pertencem ao MVP.
- Estados de tarefa e transições permitidas.
- Regras de papéis, permissões, alcance do Admin, associação a projetos e atribuição de tarefas.
- Validar que tarefas em aberto são as que não estão “Concluídas” e se o progresso deve incluir percentagens.
- Requisitos mínimos e mensuráveis de segurança, privacidade, disponibilidade e desempenho.
- Como criar, convidar, desativar e remover utilizadores; o MVP atual só descreve a gestão de papéis para utilizadores existentes.
- Como tratar atualizações concorrentes e falhas de gravação.
