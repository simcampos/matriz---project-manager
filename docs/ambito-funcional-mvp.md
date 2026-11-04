# Âmbito funcional — Matriz

## Objetivo e pressupostos

Este documento propõe um âmbito inicial para uma aplicação web de gestão de projetos e tarefas. Parte dos pressupostos fornecidos para o MVP: três tipos de utilizador (Admin, Project Manager e Developer), equipas pequenas ou médias, acesso por browser, autenticação por email e palavra-passe e ausência de integrações externas.

O âmbito funcional desta fase é o definido na ficha de implementação. As funcionalidades constam do âmbito. Para a estrutura inicial estão confirmados sessões Django, códigos/defaults de estado e prioridade e eliminação em cascata; regras de acesso, elegibilidade e cardinalidade que não foram fixadas continuam propostas para validação. O MVP não inclui personalização avançada nem dependências externas.

## Tipos de utilizador e responsabilidades

| Tipo | Responsabilidades propostas |
|---|---|
| **Admin** | Consultar utilizadores existentes e atribuir papéis; o alcance do acesso administrativo a projetos ainda precisa de confirmação. |
| **Project Manager** | Criar, gerir e eliminar projetos; organizar tarefas, gerir responsáveis e acompanhar o progresso. |
| **Developer** | Consultar projetos a que tem acesso; atualizar o estado das tarefas que lhe estão atribuídas e colaborar através de comentários. |

As permissões exatas e a possibilidade de um utilizador acumular papéis devem ser confirmadas com o cliente.

## Essenciais — MVP

| Funcionalidade | Descrição | Justificação | Prioridade |
|---|---|---|---|
| **Autenticação e sessão** | Acesso por email e palavra-passe, com entrada e saída através de sessões server-side Django. | Foi definido como pressuposto para o MVP e permite associar ações a uma conta. | Alta |
| **Gestão básica de utilizadores e papéis** | Admin consulta utilizadores existentes e atribui um dos papéis propostos. A criação, convite e desativação de contas não estão definidos. | Os papéis foram fornecidos como pressuposto e são necessários para distinguir responsabilidades; o ciclo de vida de contas continua em aberto. | Alta |
| **Gestão e pesquisa de projetos** | Project Manager cria, consulta, edita e elimina projetos; utilizadores pesquisam por nome entre projetos acessíveis. | Organizar e encontrar projetos é parte da utilização central. Regras de acesso e semântica de eliminação precisam de validação. | Alta |
| **Acesso de utilizadores aos projetos** | Project Manager associa membros existentes a projetos. Utilizadores não associados não podem consultar nem alterar o projeto ou as suas tarefas. | A associação torna explícito quem participa e reduz a exposição de trabalho fora do projeto. | Alta |
| **Gestão de tarefas** | Project Manager cria, consulta, edita e elimina tarefas com estado e prioridade; defaults `TODO` e `MEDIUM`. A política de eliminação em cascata está confirmada para a estrutura inicial. | Gerir tarefas é parte explícita da necessidade. | Alta |
| **Responsáveis** | Project Manager associa e remove vários responsáveis por tarefa; os utilizadores elegíveis são definidos pelas regras de acesso a aprovar. | A ficha requer atribuição múltipla. | Alta |
| **Estados e prioridades** | Estados `TODO`, `IN_PROGRESS` e `DONE`; prioridades `LOW`, `MEDIUM` e `HIGH`, com defaults `TODO` e `MEDIUM`. Developer atualiza o estado das tarefas que lhe estão atribuídas. | Estados e prioridades permitem acompanhar e ordenar o trabalho; as permissões por papel carecem de validação. | Alta |
| **Consulta e filtragem de tarefas** | Lista tarefas por projeto e permite filtrar por estado e prioridade; pode manter o filtro por responsável do MVP anterior. | Permite localizar o trabalho relevante. | Alta |
| **Comentários** | Utilizadores autorizados podem adicionar e listar comentários; cada comentário apresenta autor e data. | Dá contexto de colaboração junto da tarefa; regras de conteúdo e moderação carecem de validação. | Alta |
| **Resumo do progresso do projeto** | Mostrar contagens por estado e lista de tarefas em aberto, definida provisoriamente como tarefas cujo estado não é “Concluída”. | Dá uma leitura do progresso a partir de dados já existentes, sem criar métricas históricas. | Alta |
| **Painel inicial** | Apresentar projetos acessíveis e contagens de tarefas por estado em cada projeto. | Dá uma visão inicial do trabalho autorizado ao utilizador. | Alta |
| **Tarefas atribuídas ao utilizador** | O utilizador autenticado consulta, com filtro opcional por estado, as tarefas que lhe estão atribuídas em todos os projetos a que tem acesso. | Dá acesso rápido ao trabalho pessoal a partir do dashboard; proposta a validar. | Média |

### Limites propostos para o MVP

- Uma equipa inicial. Cerca de 50 utilizadores é uma referência de dimensionamento, não um limite funcional confirmado.
- Papéis e estados de tarefa fixos; sem fluxos personalizados.
- Informação básica de projeto e tarefa; sem campos personalizados.
- Acompanhamento ao nível do projeto através das tarefas; sem relatórios históricos.
- Sem integrações externas, automações, notificações por canais externos ou importação de dados.
- Sem arquivamento de projetos no MVP; esta necessidade requer validação.

## Futuras — fora do MVP

Estas funcionalidades poderão ser consideradas depois de validar as necessidades e prioridades com o cliente:

- **Fluxos, estados e campos personalizados:** adaptar a ferramenta a diferentes processos, caso a equipa necessite de mais flexibilidade.
- **Menções e notificações:** alertar os utilizadores sobre alterações relevantes.
- **Anexos em tarefas:** manter documentos de apoio junto do trabalho quando o cliente confirmar essa necessidade e os requisitos de armazenamento.
- **Relatórios, gráficos e histórico de progresso:** analisar tendências e evolução para além do estado atual das tarefas.
- **Vistas adicionais, como quadro visual ou calendário:** oferecer formas alternativas de organizar o trabalho se as equipas demonstrarem essa preferência.
- **Subtarefas, dependências e marcos:** representar trabalho mais complexo quando os projetos exigirem decomposição e coordenação entre tarefas.
- **Integrações externas:** ligar a aplicação a ferramentas de identidade, comunicação, calendário ou desenvolvimento após identificar os serviços necessários.
- **Escala e administração avançadas:** suportar múltiplas equipas, permissões granulares, auditoria e requisitos de retenção quando o contexto real os justificar.
- **Arquivamento de projetos:** permitir retirar projetos do fluxo ativo, se o cliente confirmar a necessidade e as regras de acesso aos projetos arquivados.

## Questões a validar antes de fechar o âmbito

- Confirmar se os papéis, responsabilidades e permissões propostos correspondem à organização do cliente.
- Confirmar os campos obrigatórios e limites de projetos e tarefas; a proposta atual é título obrigatório e descrição opcional para ambos. A implementação atual valida projetos com título de 3 a 100 caracteres e descrição até 1000, limites ainda por aprovar com o cliente.
- Confirmar se prioridade deve poder ser alterada para além dos defaults aprovados.
- Confirmar se uma tarefa pode ficar sem responsáveis e quem pode ser atribuído.
- A eliminação em cascata de dados dependentes de projetos e tarefas está confirmada; definir como a interface comunica essa consequência.
- Para esta implementação, comentários têm entre 1 e 2000 caracteres, rejeitam conteúdo só com espaços e são ordenados cronologicamente; definir edição e remoção continua pendente.
- Para esta implementação, só o gestor pode gerir responsáveis e estes têm de ser membros ativos do projeto ou o próprio gestor.
- Confirmar se tarefas em aberto são as que não estão em `DONE` e a forma de calcular/apresentar o progresso.
- Definir a regra de correspondência da pesquisa por nome.
- Confirmar se a associação de membros a projetos é suficiente ou se são necessárias equipas com acesso partilhado.
- Recolher requisitos concretos de segurança, recuperação de acesso e gestão de contas.
- Rever as funcionalidades futuras com o cliente antes de as incluir numa fase posterior.
