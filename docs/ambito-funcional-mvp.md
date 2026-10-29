# Âmbito funcional — Matriz

## Objetivo e pressupostos

Este documento propõe um âmbito inicial para uma aplicação web de gestão de projetos e tarefas. Parte dos pressupostos fornecidos pelo cliente: três tipos de utilizador (Admin, Project Manager e Developer), equipas pequenas ou médias (até cerca de 50 utilizadores), acesso por browser, autenticação por email e password e ausência de integrações externas no MVP.

Como ainda faltam respostas do cliente, as funcionalidades abaixo são propostas para validação, não requisitos confirmados. O MVP concentra-se em criar projetos, organizar tarefas e acompanhar o respetivo progresso, sem personalização avançada ou dependências externas.

## Tipos de utilizador e responsabilidades

| Tipo | Responsabilidades propostas |
|---|---|
| **Admin** | Gerir utilizadores e atribuir papéis; ter acesso administrativo aos projetos e à configuração básica da equipa. |
| **Project Manager** | Criar e gerir projetos; organizar tarefas, atribuir responsáveis e acompanhar o progresso do trabalho. |
| **Developer** | Consultar os projetos a que tem acesso; atualizar o estado e os detalhes das tarefas que lhe estão atribuídas. |

As permissões exatas e a possibilidade de um utilizador acumular papéis devem ser confirmadas com o cliente.

## Essenciais — MVP

| Funcionalidade | Descrição | Justificação | Prioridade |
|---|---|---|---|
| **Autenticação e sessão** | Acesso por email e password, com entrada e saída da aplicação. | É um pressuposto explícito e permite identificar o utilizador para aplicar permissões. | Alta |
| **Gestão de utilizadores e papéis** | Admin consulta e gere os utilizadores da equipa e atribui um dos papéis definidos para o MVP. | A aplicação precisa de distinguir responsabilidades e controlar quem pode gerir projetos e tarefas. | Alta |
| **Gestão de projetos** | Project Manager cria, consulta, edita e arquiva projetos com informação básica, como nome e descrição. | Organizar projetos é parte central da necessidade expressa pelo cliente; a informação básica evita complexidade prematura. | Alta |
| **Acesso de utilizadores aos projetos** | Project Manager associa os membros relevantes a cada projeto; os utilizadores consultam apenas projetos a que têm acesso, além do acesso administrativo do Admin. | Permite organizar o trabalho por projeto e evita expor trabalho a membros sem relação com ele. | Alta |
| **Gestão de tarefas** | Criar, consultar, editar e concluir tarefas dentro de um projeto. Cada tarefa tem, no mínimo, título, descrição, estado e responsável; prioridade e prazo são campos simples propostos. | Gerir tarefas é explicitamente parte do produto. Um conjunto pequeno de campos permite atribuir e acompanhar trabalho sem introduzir regras complexas. | Alta |
| **Estados fixos de tarefa** | Disponibilizar um fluxo simples comum, por exemplo: Por fazer, Em progresso e Concluída. O Developer atualiza o estado; o Project Manager também pode geri-lo. | Uma sequência curta de estados torna o progresso visível e útil sem exigir fluxos configuráveis no MVP. | Alta |
| **Consulta de tarefas por projeto** | Apresentar as tarefas de um projeto numa lista, com filtragem básica por estado e responsável. | Ajuda a equipa a encontrar o trabalho relevante e dá suporte à gestão diária sem exigir dashboards avançados. | Média |
| **Resumo do progresso do projeto** | Mostrar contagens de tarefas por estado e a lista de tarefas em aberto no contexto do projeto. | Dá uma leitura inicial do progresso baseada em dados que o MVP já recolhe, sem inventar métricas mais sofisticadas. | Alta |

### Limites propostos para o MVP

- Uma equipa e até cerca de 50 utilizadores, conforme o pressuposto inicial.
- Papéis e estados de tarefa fixos; sem fluxos personalizados.
- Informação básica de projeto e tarefa; sem campos personalizados.
- Acompanhamento ao nível do projeto através das tarefas; sem relatórios históricos.
- Sem integrações externas, automações, notificações por canais externos ou importação de dados.

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

## Questões a validar antes de fechar o âmbito

- Confirmar se os papéis, responsabilidades e permissões propostos correspondem à organização do cliente.
- Confirmar os campos obrigatórios de projetos e tarefas, incluindo prioridade e prazo.
- Validar os estados fixos e a forma de calcular/apresentar o progresso.
- Confirmar se a associação de membros a projetos é suficiente ou se são necessárias equipas com acesso partilhado.
- Recolher requisitos concretos de segurança, recuperação de acesso e gestão de contas.
- Rever as funcionalidades futuras com o cliente antes de as incluir numa fase posterior.
