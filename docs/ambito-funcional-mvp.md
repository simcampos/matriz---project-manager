# Âmbito funcional — Matriz

## Objetivo e pressupostos

Este documento propõe um âmbito inicial para uma aplicação web de gestão de projetos e tarefas. Parte dos pressupostos fornecidos para o MVP: três tipos de utilizador (Admin, Project Manager e Developer), equipas pequenas ou médias, acesso por browser, autenticação por email e palavra-passe e ausência de integrações externas.

Como ainda faltam respostas do cliente, as funcionalidades abaixo são propostas para validação, não requisitos confirmados. O MVP concentra-se em criar projetos, organizar tarefas e acompanhar o respetivo progresso, sem personalização avançada ou dependências externas.

## Tipos de utilizador e responsabilidades

| Tipo | Responsabilidades propostas |
|---|---|
| **Admin** | Consultar utilizadores existentes e atribuir papéis; o alcance do acesso administrativo a projetos ainda precisa de confirmação. |
| **Project Manager** | Criar e gerir projetos; organizar tarefas, atribuir responsáveis e acompanhar o progresso do trabalho. |
| **Developer** | Consultar os projetos a que tem acesso; atualizar o estado das tarefas que lhe estão atribuídas. |

As permissões exatas e a possibilidade de um utilizador acumular papéis devem ser confirmadas com o cliente.

## Essenciais — MVP

| Funcionalidade | Descrição | Justificação | Prioridade |
|---|---|---|---|
| **Autenticação e sessão** | Acesso por email e palavra-passe, com entrada e saída. | Foi definido como pressuposto para o MVP e permite associar ações a uma conta; o método continua sujeito a validação. | Alta |
| **Gestão básica de utilizadores e papéis** | Admin consulta utilizadores existentes e atribui um dos papéis propostos. A criação, convite e desativação de contas não estão definidos. | Os papéis foram fornecidos como pressuposto e são necessários para distinguir responsabilidades; o ciclo de vida de contas continua em aberto. | Alta |
| **Gestão de projetos** | Project Manager cria, consulta e edita projetos com título obrigatório e descrição opcional, conforme proposta a validar. | Organizar projetos é parte explícita da necessidade; informação básica mantém o MVP reduzido. | Alta |
| **Acesso de utilizadores aos projetos** | Project Manager associa membros existentes a projetos. Utilizadores não associados não podem consultar nem alterar o projeto ou as suas tarefas. | A associação torna explícito quem participa e reduz a exposição de trabalho fora do projeto. | Alta |
| **Gestão de tarefas** | Project Manager cria, consulta e edita tarefas dentro de um projeto. Título e estado são obrigatórios; descrição é opcional e a tarefa pode ficar sem responsável até confirmação da regra. | Gerir tarefas é parte explícita da necessidade; um conjunto mínimo de campos permite organizar o trabalho sem acrescentar campos ainda não validados. | Alta |
| **Atribuição de tarefas** | Project Manager pode atribuir uma tarefa a um membro associado ao respetivo projeto. | A atribuição está incluída no objetivo do MVP e torna explícita a responsabilidade pelo trabalho. | Alta |
| **Estados fixos de tarefa** | Usar, como proposta a validar, “Por fazer”, “Em progresso” e “Concluída”. Developer atualiza o estado das tarefas que lhe estão atribuídas; Project Manager pode editar tarefas nos projetos que gere. | Estados permitem acompanhar progresso com regras simples; a lista concreta e as permissões ainda precisam de confirmação. | Alta |
| **Consulta de tarefas por projeto** | Apresentar uma lista de tarefas, com filtragem por estado e responsável. | Uma lista dá acesso operacional às tarefas; os filtros são uma proposta de baixo custo de âmbito e devem ser confirmados. | Média |
| **Resumo do progresso do projeto** | Mostrar contagens por estado e lista de tarefas em aberto, definida provisoriamente como tarefas cujo estado não é “Concluída”. | Dá uma leitura do progresso a partir de dados já existentes, sem criar métricas históricas. | Alta |

### Limites propostos para o MVP

- Uma equipa inicial. Cerca de 50 utilizadores é uma referência de dimensionamento, não um limite funcional confirmado.
- Papéis e estados de tarefa fixos; sem fluxos personalizados.
- Informação básica de projeto e tarefa; sem campos personalizados.
- Acompanhamento ao nível do projeto através das tarefas; sem relatórios históricos.
- Sem integrações externas, automações, notificações por canais externos ou importação de dados.
- Sem arquivamento de projetos no MVP; esta necessidade requer validação.

## Futuras — fora do MVP

Estas funcionalidades poderão ser consideradas depois de validar as necessidades e prioridades com o cliente:

- **Fluxos, estados, prioridades e campos personalizados:** adaptar a ferramenta a diferentes processos, caso a equipa necessite de mais flexibilidade.
- **Comentários, menções e notificações:** apoiar colaboração contextual e alertar os utilizadores sobre alterações relevantes.
- **Anexos em tarefas:** manter documentos de apoio junto do trabalho quando o cliente confirmar essa necessidade e os requisitos de armazenamento.
- **Relatórios, gráficos e histórico de progresso:** analisar tendências e evolução para além do estado atual das tarefas.
- **Vistas adicionais, como quadro visual ou calendário:** oferecer formas alternativas de organizar o trabalho se as equipas demonstrarem essa preferência.
- **Subtarefas, dependências e marcos:** representar trabalho mais complexo quando os projetos exigirem decomposição e coordenação entre tarefas.
- **Integrações externas:** ligar a aplicação a ferramentas de identidade, comunicação, calendário ou desenvolvimento após identificar os serviços necessários.
- **Escala e administração avançadas:** suportar múltiplas equipas, permissões granulares, auditoria e requisitos de retenção quando o contexto real os justificar.
- **Arquivamento de projetos:** permitir retirar projetos do fluxo ativo, se o cliente confirmar a necessidade e as regras de acesso aos projetos arquivados.

## Questões a validar antes de fechar o âmbito

- Confirmar se os papéis, responsabilidades e permissões propostos correspondem à organização do cliente.
- Confirmar os campos obrigatórios de projetos e tarefas; a proposta atual é título obrigatório e descrição opcional para ambos, com estado obrigatório para tarefas.
- Confirmar se uma tarefa pode ficar sem responsável e se prioridade e prazo pertencem ao MVP.
- Validar os estados fixos e a forma de calcular/apresentar o progresso.
- Confirmar se a associação de membros a projetos é suficiente ou se são necessárias equipas com acesso partilhado.
- Recolher requisitos concretos de segurança, recuperação de acesso e gestão de contas.
- Rever as funcionalidades futuras com o cliente antes de as incluir numa fase posterior.
