# User Stories — Matriz

## Contexto

Este backlog detalha o âmbito da ficha de implementação: autenticação, gestão e pesquisa de projetos, tarefas com estado e prioridade, múltiplos responsáveis, comentários, gestão de papéis e membros e painel inicial. As regras de acesso aprovadas para Admin e gestão de membros estão descritas nas histórias relevantes. Para a estrutura inicial foram confirmados sessões Django, estados `TODO`/`IN_PROGRESS`/`DONE`, prioridades `LOW`/`MEDIUM`/`HIGH` com defaults `TODO`/`MEDIUM` e eliminação em cascata de dados dependentes.

**Prioridades:** Alta significa necessária para o fluxo central; Média significa útil para utilização diária, mas adiável. Admin, Project Manager e Developer são os rótulos dos papéis. Decisões ainda sujeitas a validação são identificadas como tal.

## US-01 — Autenticar-se

**Prioridade:** Alta

**Como utilizador, quero iniciar e terminar sessão com o meu email e palavra-passe, para aceder à aplicação de forma identificada.**

**Critérios de aceitação**

1. **Given** uma conta ativa existente e as credenciais corretas, **When** o utilizador submete o formulário de entrada, **Then** a sessão é iniciada e o utilizador acede à aplicação autenticado.
2. **Given** um email não registado ou uma palavra-passe incorreta, **When** o utilizador tenta iniciar sessão, **Then** o acesso não é concedido e a mesma mensagem genérica é apresentada nos dois casos.
3. **Given** uma sessão autenticada, **When** o utilizador escolhe terminar sessão, **Then** a sessão atual termina e uma nova consulta a um recurso protegido não apresenta o respetivo conteúdo até nova autenticação.
4. **Given** uma sessão autenticada, **When** o utilizador consulta a sua própria conta, **Then** são apresentados o seu email e o seu papel.

## US-02 — Consultar projetos acessíveis

**Prioridade:** Alta

**Como Developer, quero consultar os projetos a que tenho acesso, para encontrar o contexto do trabalho atribuído à minha equipa.**

**Critérios de aceitação**

1. **Given** um Developer associado a projetos, **When** consulta a lista de projetos, **Then** são apresentados os projetos a que está associado e nenhum projeto não associado.
2. **Given** um utilizador autenticado sem associação a um projeto, **When** consulta a lista ou tenta aceder diretamente ao projeto, **Then** os dados do projeto e das respetivas tarefas não são apresentados.
3. **Given** um Admin autenticado, **When** consulta projetos, tarefas, responsáveis ou comentários, **Then** pode ler os dados de todos os projetos, mas não pode alterar projetos/tarefas, gerir responsáveis ou adicionar comentários.

O acesso a projetos arquivados ainda não está definido; não é critério aprovado desta história.

## US-03 — Criar e gerir projetos

**Prioridade:** Alta

**Como Project Manager, quero criar, atualizar e eliminar projetos, para organizar o trabalho da equipa por objetivo.**

**Critérios de aceitação**

1. **Given** um Project Manager autenticado, **When** submete um título com 3 a 100 caracteres e pelo menos um carácter diferente de espaço, **Then** o projeto é criado e o título guardado corresponde ao valor submetido sem espaços no início e no fim.
2. **Given** um projeto existente que o Project Manager pode gerir, **When** altera e guarda o título ou a descrição, **Then** os novos valores são apresentados na consulta do projeto.
3. **Given** um formulário de projeto com título vazio ou composto apenas por espaços, **When** o utilizador tenta guardar, **Then** o projeto não é criado ou alterado e é apresentada uma indicação de que o título é obrigatório.
4. **Given** um Developer autenticado, **When** tenta criar ou editar um projeto, **Then** a operação é recusada e os dados do projeto permanecem inalterados.
5. **Given** um projeto que o Project Manager pode gerir, **When** pede a sua eliminação, **Then** a operação é autorizada e as tarefas, associações, responsáveis e comentários dependentes são removidos em cascata.

Título obrigatório, descrição opcional e a regra de quem pode eliminar são propostas para confirmação. A implementação e o contrato atuais limitam o título a 3–100 caracteres e a descrição a 1000 caracteres; estes limites e as regras de acesso ainda precisam de validação do cliente.

## US-04 — Criar e gerir tarefas

**Prioridade:** Alta

**Como Project Manager, quero criar, consultar, atualizar e eliminar tarefas num projeto, para decompor o trabalho em atividades acompanháveis.**

**Critérios de aceitação**

1. **Given** um Project Manager com acesso de gestão a um projeto, **When** cria uma tarefa com título de 3 a 150 caracteres que não seja só espaços, descrição opcional até 2000 caracteres e, opcionalmente, estado e prioridade permitidos, **Then** a tarefa fica associada ao projeto; os valores omitidos assumem `TODO` e `MEDIUM`.
2. **Given** uma tarefa existente num projeto que pode gerir, **When** atualiza o título, a descrição opcional, o estado ou a prioridade para valores permitidos e guarda, **Then** os novos valores são apresentados na consulta da tarefa.
3. **Given** uma tarefa com título inválido ou estado/prioridade fora dos valores permitidos, **When** o utilizador tenta criá-la ou guardar alterações, **Then** a operação é recusada, a tarefa não é criada ou mantém os valores anteriores e é apresentada uma indicação do campo inválido.
4. **Given** um utilizador sem associação ao projeto da tarefa, **When** tenta consultá-la ou alterá-la, **Then** os dados não são apresentados e nenhum valor é alterado.
5. **Given** um Project Manager com acesso de gestão à tarefa, **When** pede a sua eliminação, **Then** a tarefa deixa de estar disponível e os seus responsáveis e comentários são removidos em cascata.

O título tem de conter entre 3 e 150 caracteres após remover espaços externos e não pode ser composto apenas por espaços. A descrição é opcional e tem no máximo 2000 caracteres. Estado e prioridade têm defaults `TODO` e `MEDIUM`; os códigos aceites são `TODO`/`IN_PROGRESS`/`DONE` e `LOW`/`MEDIUM`/`HIGH`. As regras de acesso continuam conforme a matriz de permissões a validar.

## US-05 — Atribuir tarefas

**Prioridade:** Alta

**Como Project Manager, quero associar e remover vários responsáveis de uma tarefa, para tornar explícita a responsabilidade partilhada pelo trabalho.**

**Critérios de aceitação**

1. **Given** uma tarefa e um utilizador ativo que é membro do projeto ou o seu gestor, **When** o Project Manager o associa, **Then** o responsável aparece uma única vez; repetir a associação devolve conflito e não duplica a relação.
2. **Given** uma tarefa com responsáveis, **When** um utilizador com acesso ao projeto consulta a lista, **Then** todos os responsáveis atuais são apresentados.
3. **Given** um utilizador inativo ou sem associação ao projeto, **When** o Project Manager tenta atribuí-lo, **Then** a alteração é recusada e a lista anterior permanece inalterada.
4. **Given** uma tarefa com responsáveis, **When** o Project Manager remove a atribuição de um deles, **Then** esse utilizador deixa de constar e os restantes não são alterados.
5. **Given** uma tarefa, **When** o Project Manager remove todos os responsáveis, **Then** o resultado segue a regra de cardinalidade aprovada para a tarefa.

O Project Manager é o único que pode gerir responsáveis. Para esta implementação, o utilizador confirmou como elegíveis os membros ativos do projeto e o gestor. A lista pode ficar vazia; a atribuição individual duplicada devolve conflito. O gestor conta implicitamente como membro.

## US-06 — Atualizar o estado de uma tarefa

**Prioridade:** Alta

**Como Developer, quero atualizar o estado de uma tarefa que me foi atribuída, para refletir o progresso do meu trabalho.**

**Critérios de aceitação**

1. **Given** uma tarefa atribuída ao Developer e acessível por ele, **When** altera o estado para um dos estados disponíveis e guarda, **Then** o estado atualizado é apresentado na tarefa.
2. **Given** uma tarefa atribuída a outro utilizador, **When** o Developer tenta atualizar o seu estado, **Then** a alteração é recusada e o estado existente permanece inalterado.
3. **Given** um estado que não pertence à lista de estados permitidos, **When** é submetida uma tentativa de atualização, **Then** a alteração é recusada e o estado válido anterior é mantido.
4. **Given** um Project Manager que gere o projeto da tarefa, **When** atualiza o estado da tarefa para um dos estados permitidos, **Then** o novo estado é apresentado na tarefa.

Os estados confirmados para a estrutura inicial são `TODO`, `IN_PROGRESS` e `DONE`, apresentados como “Por fazer”, “Em progresso” e “Concluída”. Transições adicionais ou restrições de fluxo não foram definidas.

## US-07 — Consultar progresso do projeto

**Prioridade:** Alta

**Como membro com acesso a um projeto (por exemplo, Project Manager ou Developer), quero ver as tarefas agrupadas por estado num projeto, para acompanhar o progresso sem calcular os totais manualmente.**

**Critérios de aceitação**

1. **Given** um projeto acessível com tarefas nos estados permitidos, **When** um utilizador com acesso ao projeto consulta o resumo do projeto, **Then** é apresentado um total para cada estado e a lista contém exatamente as tarefas cujo estado não é “Concluída”.
2. **Given** um projeto sem tarefas, **When** um utilizador com acesso ao projeto consulta o resumo, **Then** cada total apresentado é zero e a lista de tarefas em aberto está vazia.
3. **Given** uma tarefa cujo estado foi alterado e guardado, **When** o resumo do projeto é consultado novamente, **Then** os totais refletem o estado atual da tarefa e cada tarefa é contada uma única vez.
4. **Given** um utilizador sem acesso ao projeto, **When** tenta consultar o resumo, **Then** os totais e as tarefas do projeto não são apresentados.

O resumo é visível a qualquer utilizador com acesso ao projeto (decisão adotada na Ficha PL 02, a validar com o cliente).

## US-08 — Gerir utilizadores e papéis

**Prioridade:** Alta

**Como Admin, quero consultar os utilizadores da equipa e atribuir-lhes papéis, para manter as responsabilidades e os acessos organizados.**

**Critérios de aceitação**

1. **Given** um Admin autenticado, **When** consulta os utilizadores existentes da equipa, **Then** a lista apresenta cada utilizador e o papel atualmente atribuído.
2. **Given** um utilizador existente e um dos papéis permitidos (Admin, Project Manager ou Developer), **When** o Admin atribui e guarda esse papel, **Then** o novo papel fica associado ao utilizador e é apresentado na consulta seguinte.
3. **Given** um Developer autenticado, **When** tenta consultar ou alterar papéis de utilizadores, **Then** a operação é recusada e os papéis existentes permanecem inalterados.
4. **Given** um papel que não pertence aos três papéis permitidos, **When** o Admin tenta atribuí-lo, **Then** a alteração é recusada e o papel anterior permanece inalterado.
5. **Given** um utilizador que gere pelo menos um projeto, **When** o Admin tenta atribuir-lhe um papel diferente de Project Manager, **Then** a alteração é recusada e o papel anterior permanece inalterado.
6. **Given** o último Admin ativo, **When** outro Admin tenta alterar o seu papel para não-Admin, **Then** a operação é recusada e permanece pelo menos um Admin ativo.

## US-09 — Associar membros a projetos

**Prioridade:** Alta

**Como Project Manager, quero associar membros a um projeto que posso gerir, para que apenas as pessoas relevantes tenham acesso ao trabalho desse projeto.**

**Critérios de aceitação**

1. **Given** um Project Manager com acesso de gestão a um projeto e um utilizador ativo de qualquer papel, **When** associa esse utilizador ao projeto, **Then** o utilizador passa a constar uma única vez na lista de membros do projeto.
2. **Given** um utilizador associado a um projeto, **When** consulta os projetos disponíveis, **Then** o projeto associado é apresentado.
3. **Given** um utilizador sem associação ao projeto, **When** consulta os projetos disponíveis ou tenta aceder diretamente ao projeto, **Then** o projeto não é apresentado e os dados do projeto e das tarefas não ficam acessíveis.
4. **Given** um Developer autenticado, **When** tenta alterar a associação de membros a um projeto, **Then** a operação é recusada e a lista de membros permanece inalterada.
5. **Given** um utilizador que já é membro do projeto ou que é o seu gestor, **When** o Project Manager tenta associá-lo novamente, **Then** a operação é recusada por conflito e a lista de membros permanece inalterada.
6. **Given** um membro associado ao projeto, **When** o Project Manager o remove, **Then** deixa de ter acesso ao projeto e são removidas as suas atribuições às tarefas desse projeto.
7. **Given** um utilizador que não é o Project Manager responsável, **When** tenta adicionar ou remover membros, **Then** a operação é recusada e a composição do projeto não se altera.

O gestor do projeto conta implicitamente como membro: aparece na lista e não pode ser removido. Remover outro membro elimina as respetivas atribuições às tarefas do projeto.

## US-10 — Consultar e filtrar tarefas

**Prioridade:** Média

**Como membro associado a um projeto, quero consultar e filtrar as tarefas por estado e prioridade, para localizar o trabalho relevante.**

**Critérios de aceitação**

1. **Given** um utilizador associado a um projeto com tarefas, **When** consulta a lista de tarefas desse projeto, **Then** são apresentadas as tarefas desse projeto e nenhuma tarefa de outro projeto.
2. **Given** a lista de tarefas de um projeto e um estado permitido selecionado, **When** aplica o filtro de estado, **Then** cada tarefa apresentada tem exatamente esse estado.
3. **Given** a lista de tarefas de um projeto e uma prioridade permitida selecionada, **When** aplica o filtro de prioridade, **Then** cada tarefa apresentada tem exatamente essa prioridade.
4. **Given** a lista de tarefas de um projeto e um responsável selecionado, **When** aplica o filtro de responsável, **Then** cada tarefa apresentada inclui esse responsável.
5. **Given** nenhum resultado correspondente aos filtros escolhidos, **When** os filtros são aplicados, **Then** a lista não apresenta tarefas e indica que não existem resultados.

O âmbito também permite manter o filtro por responsável do MVP anterior. Os códigos de prioridade confirmados para a estrutura inicial são `LOW`, `MEDIUM` e `HIGH`, com default `MEDIUM`.

## US-11 — Consultar as minhas tarefas

**Prioridade:** Média

**Como utilizador autenticado, quero consultar as tarefas que me estão atribuídas em todos os projetos a que tenho acesso, para aceder rapidamente ao meu trabalho.**

**Critérios de aceitação**

1. **Given** um utilizador com tarefas atribuídas em vários projetos a que tem acesso, **When** consulta as suas tarefas, **Then** são apresentadas todas as tarefas atribuídas a si, com o respetivo estado, e nenhuma tarefa atribuída a outros utilizadores.
2. **Given** as tarefas atribuídas ao utilizador e um estado permitido selecionado, **When** aplica o filtro de estado, **Then** cada tarefa apresentada tem exatamente esse estado.
3. **Given** um utilizador sem tarefas atribuídas, **When** consulta as suas tarefas, **Then** a lista não apresenta tarefas e indica que não existem resultados.

Proposta acrescentada na Ficha PL 02 para suportar o dashboard; a validar com o cliente.

## US-12 — Consultar o painel inicial

**Prioridade:** Alta

**Como utilizador autenticado, quero consultar os projetos a que tenho acesso e as contagens de tarefas por estado, para obter uma visão inicial do trabalho disponível.**

**Critérios de aceitação**

1. **Given** um utilizador autenticado com projetos acessíveis, **When** abre o painel inicial, **Then** são apresentados apenas os seus projetos acessíveis e as contagens de tarefas por estado de cada projeto.
2. **Given** um projeto acessível sem tarefas, **When** o painel é apresentado, **Then** as contagens desse projeto são zero.
3. **Given** um utilizador sem projetos acessíveis, **When** abre o painel, **Then** é apresentado um estado vazio sem revelar projetos alheios.

## US-13 — Comentar uma tarefa

**Prioridade:** Alta

**Como utilizador com acesso ao projeto, quero adicionar e consultar comentários numa tarefa, para manter a conversa junto do trabalho.**

**Critérios de aceitação**

1. **Given** um utilizador com acesso ao projeto, **When** adiciona conteúdo entre 1 e 2000 caracteres que não seja só espaços, **Then** o comentário é guardado com o autor autenticado e a data atribuída pelo sistema.
2. **Given** uma tarefa com comentários, **When** um utilizador autorizado consulta os comentários, **Then** cada comentário apresenta conteúdo, autor e data, por ordem cronológica ascendente.
3. **Given** um utilizador sem acesso ao projeto, **When** tenta consultar ou adicionar comentários, **Then** a operação é recusada e nenhum comentário é revelado ou criado.

O limite de 1–2000 caracteres, a rejeição de conteúdo só com espaços e a ordem cronológica ascendente estão confirmados para esta implementação. Edição, remoção e retenção de comentários continuam por definir.

## US-14 — Pesquisar projetos

**Prioridade:** Alta

**Como utilizador autenticado, quero pesquisar projetos pelo nome, para encontrar rapidamente um projeto a que tenho acesso.**

**Critérios de aceitação**

1. **Given** projetos acessíveis com nomes correspondentes à pesquisa, **When** o utilizador pesquisa pelo nome, **Then** são apresentados apenas os projetos acessíveis que correspondem.
2. **Given** que não existem correspondências acessíveis, **When** a pesquisa é executada, **Then** a lista fica vazia e indica que não há resultados.
3. **Given** um projeto não acessível que corresponde ao termo, **When** o utilizador pesquisa, **Then** o projeto não é apresentado.

A regra de correspondência (parcial/exata, maiúsculas e acentos) e o comprimento mínimo da pesquisa precisam de confirmação.

## Casos excecionais relevantes

1. **Credenciais inválidas:** negar acesso e não revelar se o email está registado.
2. **Acesso indevido:** utilizadores sem associação ao projeto não podem consultar nem alterar o projeto, as tarefas ou o resumo, incluindo através de acesso direto.
3. **Responsável não elegível:** impedir a associação a alguém que não esteja autorizado e preservar a lista anterior de responsáveis.
4. **Campos obrigatórios em falta:** recusar a gravação e não criar registos incompletos.
5. **Projeto sem tarefas:** mostrar totais iguais a zero e uma lista em aberto vazia.
6. **Eliminação:** eliminar em cascata tarefas, associações, responsáveis e comentários dependentes, conforme decisão da estrutura inicial.
7. **Atualizações concorrentes:** não existe regra definida para duas pessoas alterarem a mesma tarefa antes de qualquer delas guardar; decidir como prevenir perda silenciosa de alterações.

## Questões por confirmar

- Confirmar possibilidade de acumular papéis e as transições de estado das tarefas.
- Definir como criar, convidar, desativar e remover utilizadores. US-08 cobre apenas utilizadores existentes; o mecanismo de disponibilização das primeiras contas é um bloqueio em aberto.
- Confirmar regras propostas: título obrigatório e descrição opcional para projetos e tarefas.
- Confirmar se tarefas podem ficar sem responsáveis.
- Confirmar a elegibilidade de responsáveis e a cardinalidade mínima/máxima; a ficha exige suporte para vários responsáveis.
- Confirmar se “em aberto” significa estado diferente de `DONE`.
- Definir pesquisa por nome e validação de comentários.
- Definir comportamento de projeto arquivado; o arquivamento foi retirado do MVP até confirmação.
- Definir resultado verificável para falhas de gravação e alterações simultâneas.
- Definir limites de tamanho dos campos para que a validação de conteúdo fique totalmente objetiva.
- Validar com o cliente as decisões adotadas na Ficha PL 02: gestor único por projeto que conta implicitamente como membro; recusa de alterar o papel de quem gere projetos; resumo de progresso visível a qualquer utilizador com acesso ao projeto; sessão invalidada no servidor ao terminar sessão; vista "As minhas tarefas" (US-11).
