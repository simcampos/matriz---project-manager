# Restrições e pressupostos — Matriz

## Factos explicitamente comunicados pelo cliente

- O cliente precisa de uma aplicação para as suas equipas.
- As equipas devem poder organizar projetos, gerir tarefas e acompanhar o progresso do trabalho.

## Pressupostos fornecidos para o MVP

- O acesso será feito através de um browser web.
- Os perfis considerados são Admin, Project Manager e Developer.
- A escala de referência é uma equipa pequena/média, até cerca de 50 utilizadores; não é um limite funcional confirmado.
- A autenticação é por email e palavra-passe; a implementação inicial usa sessões Django servidor-side.
- Não haverá integrações externas no MVP.
- O MVP deve cobrir autenticação, gestão de projetos e tarefas, atribuição de tarefas e visualização de progresso.
- O âmbito desta fase, conforme a ficha de implementação, inclui operações CRUD de projetos e tarefas, prioridade, múltiplos responsáveis por tarefa, comentários, pesquisa de projetos por nome, filtros de tarefas por estado/prioridade e painel inicial com projetos acessíveis e contagens por estado.
- Stack escolhida para a implementação inicial: Python, Django, Django REST Framework, React, Vite, PostgreSQL e Django ORM, num monólito modular ([architecture.md](./architecture.md)).

## Decisões confirmadas para a estrutura inicial

- Stack: Python, Django/DRF, React/Vite, PostgreSQL e Django ORM, num monólito modular.
- Autenticação por email e palavra-passe com sessões Django armazenadas no servidor.
- Códigos persistidos de estado `TODO`, `IN_PROGRESS`, `DONE`; de prioridade `LOW`, `MEDIUM`, `HIGH`; defaults `TODO` e `MEDIUM`.
- Eliminação em cascata de dados dependentes de projetos e tarefas; os projetos com gestor e comentários com autor impedem a eliminação desse utilizador (`PROTECT`).
- O Admin pode consultar todos os projetos, tarefas, responsáveis e comentários, mas não pode alterar projetos/tarefas, gerir responsáveis nem adicionar comentários.
- O Admin pode listar utilizadores e alterar papéis existentes; não pode rebaixar o último Admin ativo nem retirar o papel Project Manager a um utilizador que gere projetos.
- O Project Manager responsável pode associar utilizadores ativos de qualquer papel aos projetos que gere. O gestor conta implicitamente como membro e não pode ser removido; remover outro membro também remove as suas atribuições às tarefas do projeto.

## Pressupostos de produto ainda por validar

- O MVP começa com uma equipa; suportar várias equipas fica fora do âmbito inicial.
- Cada utilizador tem um papel principal entre Admin, Project Manager e Developer; acumulação de papéis não está definida. Os códigos persistidos são `ADMIN`, `PROJECT_MANAGER` e `DEVELOPER`.
- A possibilidade de acumular papéis ainda não está definida.
- Project Manager gere os projetos a que tem acesso e associa/remove utilizadores ativos como membros.
- Cada projeto tem um único Project Manager responsável, que conta implicitamente como membro do projeto. O papel de quem gere projetos não pode ser alterado para outro papel.
- Duração e expiração da sessão continuam por definir.
- O resumo de progresso de um projeto é visível a qualquer utilizador com acesso a esse projeto.
- Developer consulta projetos aos quais está associado e atualiza o estado das tarefas que lhe foram atribuídas.
- Uma tarefa pertence a um único projeto e pode ter vários responsáveis. Para esta implementação, são elegíveis membros ativos do projeto e o gestor; só o gestor do projeto pode associar ou remover responsáveis. A cardinalidade mínima continua por decidir.
- Título e estado obrigatórios e descrição opcional para tarefas. O título de tarefa tem entre 3 e 150 caracteres e não pode ser só espaços; a descrição tem no máximo 2000 caracteres. Título obrigatório e descrição opcional para projetos são propostas ainda por confirmar; a implementação atual valida título entre 3 e 100 caracteres e descrição até 1000 caracteres, limites também por validar com o cliente.
- Rótulos da interface para os estados: “Por fazer”, “Em progresso” e “Concluída”; para prioridades: “Baixa”, “Média” e “Alta”.
- O progresso inicial será apresentado como contagem de tarefas por estado e lista de tarefas em aberto, definida como estado diferente de `DONE`.
- Os comentários guardam autor e data definidos pelo servidor. Para esta implementação, o conteúdo tem 1–2000 caracteres, não pode ser só espaços e é ordenado do mais antigo para o mais recente; edição, remoção e retenção continuam por definir.
- “Até cerca de 50 utilizadores” é uma referência de dimensionamento fornecida para o MVP, não um limite máximo funcional acordado.
- Campos, permissões e fluxos definidos nos documentos são propostas para validação, não decisões finais do cliente.

## Segurança e privacidade

### Contexto conhecido

- A autenticação prevista é por email e palavra-passe.
- Existem papéis distintos e o acesso a projetos deverá ser limitado aos utilizadores autorizados, de acordo com o âmbito funcional proposto.
- Os dados deverão incluir, pelo menos, contas de utilizador, sessões, informação de projetos e informação de tarefas.
- Não foram fornecidos requisitos específicos de privacidade, proteção de dados, auditoria ou retenção.

### Regras propostas para validação

- Não apresentar nem permitir alterar projetos, tarefas ou progresso a utilizadores sem autorização para o projeto.
- Recusar alterações que o papel do utilizador não permite.
- Confirmar quais dados pessoais são necessários, quem pode consultá-los e por quanto tempo são conservados.
- Confirmar requisitos aplicáveis de auditoria, eliminação de contas/dados e resposta a incidentes.

As regras acima não especificam mecanismos de implementação e não devem ser interpretadas como requisitos técnicos fechados.

### Matriz de permissões aprovada para esta implementação

| Ação | Proposta |
|---|---|
| Criar projeto | Project Manager; o utilizador autenticado fica como gestor responsável. |
| Consultar projetos, tarefas, responsáveis e comentários | Gestor responsável, membros associados e Admin; o Admin tem acesso global apenas de leitura. |
| Editar/eliminar projeto | Apenas o gestor responsável; Admin não pode alterar. |
| Criar/editar/eliminar tarefa | Apenas o gestor responsável pelo projeto; Admin não pode alterar. |
| Consultar tarefa/comentários | Utilizadores com acesso ao projeto e Admin. |
| Alterar estado | Developer apenas numa tarefa que lhe está atribuída; o gestor do projeto pode alterar tarefas do seu projeto. |
| Comentar | Utilizadores com acesso ao projeto, exceto Admin. |
| Associar/remover responsáveis | Apenas o gestor do projeto; membros ativos do projeto ou o gestor (confirmado para esta implementação). |
| Gerir membros | Apenas o Project Manager responsável; utilizadores ativos de qualquer papel podem ser adicionados. Remover um membro também remove as suas atribuições no projeto. |

O gestor conta implicitamente como membro e como responsável elegível; membros não podem gerir atribuições ou a composição do projeto.

### Propostas mínimas de segurança por aprovar

- Uma tentativa sem autorização não deve revelar nem permitir alterar os dados do projeto, das tarefas ou do resumo.
- Mensagens de autenticação não devem indicar se o email está registado.
- Credenciais e sessões devem ser protegidas; a política concreta, recuperação de conta, expiração de sessão e prevenção de tentativas abusivas precisam de definição antes da produção. A implementação web usa cookie de sessão Django e proteção CSRF.

### Privacidade por definir

Antes da produção, identificar os dados pessoais tratados, a finalidade de cada dado, quem pode aceder, a retenção e eliminação e quaisquer requisitos legais aplicáveis. Nenhum prazo ou obrigação legal específico foi fornecido.

## Decisões técnicas ainda pendentes

- Estratégia de recuperação de acesso, duração das sessões Django e proteção contra tentativas abusivas.
- Valores seguros para produção, rotação de `SECRET_KEY`, CORS/CSRF e configuração operacional.
- Para desenvolvimento local, a aplicação é executada por Docker Compose. As imagens incluem um target backend de produção servido por Gunicorn; o workflow [release.yml](../.github/workflows/release.yml) publica-as no GHCR a partir de tags `v*.*.*`, usando `GITHUB_TOKEN`. A configuração de protótipo no Render fica em [render.yaml](../render.yaml), com região Frankfurt e planos gratuitos; estes não são adequados a produção, e a base de dados gratuita expira ao fim de 30 dias. O workflow [ci.yml](../.github/workflows/ci.yml) só aciona deploys no Render em pushes para `main`, após testes e build bem-sucedidos, usando o SHA exato testado; o job de deploy é ignorado enquanto os IDs dos dois serviços não estiverem configurados. O primeiro Apply do Blueprint inicia o deploy inicial. No perfil gratuito, migrations continuam explícitas; os segredos e IDs dos serviços são configurados no GitHub Environment `production`, nunca no repositório.
- Estratégia de testes, observabilidade, backups e recuperação.
- Browsers e versões que serão suportados.

Não substituir a stack escolhida sem aprovação.

## Limitações de âmbito

O MVP está limitado a:

- Uma equipa inicial; cerca de 50 utilizadores é apenas a escala de referência, não um limite funcional.
- Utilização através de browser web.
- Autenticação por email e palavra-passe.
- Gestão básica de projetos e tarefas, atribuição e acompanhamento do progresso atual.
- Papéis e estados de tarefa fixos, sem fluxos personalizados.
- Resumo de progresso baseado nas tarefas atuais, sem análise histórica.
- Ausência de integrações externas.
- Sem arquivamento de projetos até confirmação da necessidade e das regras de acesso.

Ficam fora do âmbito inicial: notificações, menções, anexos, automações, importação, relatórios históricos, gráficos de tendência, vistas adicionais, subtarefas, dependências, marcos, múltiplas equipas e permissões granulares. Comentários fazem parte do âmbito, mas as suas regras detalhadas e a ordenação/semântica da prioridade ainda estão por definir.

## Questões abertas

- Confirmar possibilidade de acumular papéis e transições de estado das tarefas.
- Validar com o cliente as restantes decisões de produto adotadas nesta implementação, incluindo gestor único com associação implícita e visibilidade do progresso.
- Confirmar os campos obrigatórios e se tarefas podem ficar sem responsável.
- Definir como a interface confirma eliminações em cascata.
- Definir o conteúdo, ordenação, validação, edição, remoção e retenção de comentários.
- Definir regras de pesquisa por nome e comportamento dos filtros.
- Definir o ciclo de vida de contas, recuperação de acesso e proteção de sessões.
- Definir dados pessoais tratados, finalidade, retenção e eliminação.
- Definir critérios verificáveis de segurança e privacidade.
- Definir objetivos mensuráveis de desempenho, disponibilidade, acessibilidade e compatibilidade.
- Confirmar se a escala de referência e o limite de uma equipa são adequados.
- Definir como tratar projetos arquivados, utilizadores removidos, falhas de gravação e alterações concorrentes.
