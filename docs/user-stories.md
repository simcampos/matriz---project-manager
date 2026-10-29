# User Stories — Matriz

## Contexto

Este backlog detalha o âmbito proposto para o MVP: autenticação, gestão de projetos e tarefas, atribuição de tarefas e visualização de progresso. As histórias e regras de acesso são propostas, não requisitos aprovados, e devem ser revistas pelo cliente.

**Prioridades:** Alta significa necessária para o fluxo central proposto; Média significa útil para utilização diária, mas adiável. Os nomes Admin, Project Manager e Developer são rótulos provisórios dos papéis. Os campos e estados usados nos critérios também são propostas a confirmar.

## US-01 — Autenticar-se

**Prioridade:** Alta

**Como utilizador, quero iniciar e terminar sessão com o meu email e palavra-passe, para aceder à aplicação de forma identificada.**

**Critérios de aceitação**

1. **Given** uma conta ativa existente e as credenciais corretas, **When** o utilizador submete o formulário de entrada, **Then** a sessão é iniciada e o utilizador acede à aplicação autenticado.
2. **Given** um email não registado ou uma palavra-passe incorreta, **When** o utilizador tenta iniciar sessão, **Then** o acesso não é concedido e a mesma mensagem genérica é apresentada nos dois casos.
3. **Given** uma sessão autenticada, **When** o utilizador escolhe terminar sessão, **Then** a sessão atual termina e uma nova consulta a um recurso protegido não apresenta o respetivo conteúdo até nova autenticação.

## US-02 — Consultar projetos acessíveis

**Prioridade:** Alta

**Como Developer, quero consultar os projetos a que tenho acesso, para encontrar o contexto do trabalho atribuído à minha equipa.**

**Critérios de aceitação**

1. **Given** um Developer associado a projetos, **When** consulta a lista de projetos, **Then** são apresentados os projetos a que está associado e nenhum projeto não associado.
2. **Given** um utilizador autenticado sem associação a um projeto, **When** consulta a lista ou tenta aceder diretamente ao projeto, **Then** os dados do projeto e das respetivas tarefas não são apresentados.

O âmbito de consulta de projetos pelo Admin e o acesso a projetos arquivados ainda não estão definidos; não são critérios aprovados desta história.

## US-03 — Criar e gerir projetos

**Prioridade:** Alta

**Como Project Manager, quero criar e atualizar projetos, para organizar o trabalho da equipa por objetivo.**

**Critérios de aceitação**

1. **Given** um Project Manager autenticado, **When** submete um título que contém pelo menos um carácter diferente de espaço, **Then** o projeto é criado e o título guardado corresponde ao valor submetido sem espaços no início e no fim.
2. **Given** um projeto existente que o Project Manager pode gerir, **When** altera e guarda o título ou a descrição, **Then** os novos valores são apresentados na consulta do projeto.
3. **Given** um formulário de projeto com título vazio ou composto apenas por espaços, **When** o utilizador tenta guardar, **Then** o projeto não é criado ou alterado e é apresentada uma indicação de que o título é obrigatório.
4. **Given** um Developer autenticado, **When** tenta criar ou editar um projeto, **Then** a operação é recusada e os dados do projeto permanecem inalterados.

Título obrigatório e descrição opcional são regras propostas para confirmação. Limites de tamanho e regras para descrição ainda não estão definidos.

## US-04 — Criar e gerir tarefas

**Prioridade:** Alta

**Como Project Manager, quero criar e atualizar tarefas num projeto, para decompor o trabalho em atividades acompanháveis.**

**Critérios de aceitação**

1. **Given** um Project Manager com acesso de gestão a um projeto, **When** cria uma tarefa com título que contém pelo menos um carácter diferente de espaço e com um estado permitido, **Then** a tarefa fica associada ao projeto e são apresentados o título sem espaços no início e no fim e o estado escolhido.
2. **Given** uma tarefa existente num projeto que pode gerir, **When** atualiza o título, a descrição opcional ou o estado para valores permitidos e guarda, **Then** os novos valores são apresentados na consulta da tarefa.
3. **Given** uma tarefa sem título ou sem estado permitido, **When** o utilizador tenta criá-la ou guardar alterações, **Then** a operação é recusada, a tarefa não é criada ou mantém os valores anteriores e é apresentada uma indicação do campo inválido.
4. **Given** um utilizador sem associação ao projeto da tarefa, **When** tenta consultá-la ou alterá-la, **Then** os dados não são apresentados e nenhum valor é alterado.

Título e estado obrigatórios e descrição opcional são regras propostas. O conjunto concreto de estados e limites de tamanho precisam de confirmação.

## US-05 — Atribuir tarefas

**Prioridade:** Alta

**Como Project Manager, quero atribuir uma tarefa a um membro associado ao projeto, para tornar explícita a responsabilidade pelo trabalho.**

**Critérios de aceitação**

1. **Given** uma tarefa num projeto e um membro associado a esse projeto, **When** o Project Manager atribui a tarefa a esse membro e guarda, **Then** o identificador do membro fica registado como responsável e é apresentado na consulta da tarefa.
2. **Given** uma tarefa atribuída, **When** um utilizador com acesso ao projeto consulta a tarefa, **Then** o responsável atual é apresentado.
3. **Given** um utilizador que não está associado ao projeto, **When** o Project Manager tenta atribuir-lhe a tarefa, **Then** a atribuição é recusada e o responsável anterior não é alterado.
4. **Given** uma tarefa sem responsável, **When** o Project Manager guarda a tarefa sem selecionar um membro, **Then** a tarefa permanece sem responsável. A opcionalidade do responsável é uma proposta a confirmar.

## US-06 — Atualizar o estado de uma tarefa

**Prioridade:** Alta

**Como Developer, quero atualizar o estado de uma tarefa que me foi atribuída, para refletir o progresso do meu trabalho.**

**Critérios de aceitação**

1. **Given** uma tarefa atribuída ao Developer e acessível por ele, **When** altera o estado para um dos estados disponíveis e guarda, **Then** o estado atualizado é apresentado na tarefa.
2. **Given** uma tarefa atribuída a outro utilizador, **When** o Developer tenta atualizar o seu estado, **Then** a alteração é recusada e o estado existente permanece inalterado.
3. **Given** um estado que não pertence à lista de estados permitidos, **When** é submetida uma tentativa de atualização, **Then** a alteração é recusada e o estado válido anterior é mantido.
4. **Given** um Project Manager que gere o projeto da tarefa, **When** atualiza o estado da tarefa para um dos estados permitidos, **Then** o novo estado é apresentado na tarefa.

Os três estados propostos são “Por fazer”, “Em progresso” e “Concluída”; confirmar nomes e transições com o cliente.

## US-07 — Consultar progresso do projeto

**Prioridade:** Alta

**Como Project Manager, quero ver as tarefas agrupadas por estado num projeto, para acompanhar o progresso sem calcular os totais manualmente.**

**Critérios de aceitação**

1. **Given** um projeto acessível com tarefas nos estados permitidos, **When** o Project Manager consulta o resumo do projeto, **Then** é apresentado um total para cada estado e a lista contém exatamente as tarefas cujo estado não é “Concluída”.
2. **Given** um projeto sem tarefas, **When** o Project Manager consulta o resumo, **Then** cada total apresentado é zero e a lista de tarefas em aberto está vazia.
3. **Given** uma tarefa cujo estado foi alterado e guardado, **When** o resumo do projeto é consultado novamente, **Then** os totais refletem o estado atual da tarefa e cada tarefa é contada uma única vez.
4. **Given** um utilizador sem acesso ao projeto, **When** tenta consultar o resumo, **Then** os totais e as tarefas do projeto não são apresentados.

## US-08 — Gerir utilizadores e papéis

**Prioridade:** Alta

**Como Admin, quero consultar os utilizadores da equipa e atribuir-lhes papéis, para manter as responsabilidades e os acessos organizados.**

**Critérios de aceitação**

1. **Given** um Admin autenticado, **When** consulta os utilizadores existentes da equipa, **Then** a lista apresenta cada utilizador e o papel atualmente atribuído.
2. **Given** um utilizador existente e um dos papéis permitidos (Admin, Project Manager ou Developer), **When** o Admin atribui e guarda esse papel, **Then** o novo papel fica associado ao utilizador e é apresentado na consulta seguinte.
3. **Given** um Developer autenticado, **When** tenta consultar ou alterar papéis de utilizadores, **Then** a operação é recusada e os papéis existentes permanecem inalterados.
4. **Given** um papel que não pertence aos três papéis permitidos, **When** o Admin tenta atribuí-lo, **Then** a alteração é recusada e o papel anterior permanece inalterado.

## US-09 — Associar membros a projetos

**Prioridade:** Alta

**Como Project Manager, quero associar membros a um projeto que posso gerir, para que apenas as pessoas relevantes tenham acesso ao trabalho desse projeto.**

**Critérios de aceitação**

1. **Given** um Project Manager com acesso de gestão a um projeto e um utilizador existente, **When** associa esse utilizador ao projeto, **Then** o utilizador passa a constar uma única vez na lista de membros do projeto.
2. **Given** um utilizador associado a um projeto, **When** consulta os projetos disponíveis, **Then** o projeto associado é apresentado.
3. **Given** um utilizador sem associação ao projeto, **When** consulta os projetos disponíveis ou tenta aceder diretamente ao projeto, **Then** o projeto não é apresentado e os dados do projeto e das tarefas não ficam acessíveis.
4. **Given** um Developer autenticado, **When** tenta alterar a associação de membros a um projeto, **Then** a operação é recusada e a lista de membros permanece inalterada.

## US-10 — Consultar e filtrar tarefas

**Prioridade:** Média

**Como membro associado a um projeto, quero consultar e filtrar as tarefas por estado ou responsável, para localizar o trabalho relevante.**

**Critérios de aceitação**

1. **Given** um utilizador associado a um projeto com tarefas, **When** consulta a lista de tarefas desse projeto, **Then** são apresentadas as tarefas desse projeto e nenhuma tarefa de outro projeto.
2. **Given** a lista de tarefas de um projeto e um estado permitido selecionado, **When** aplica o filtro de estado, **Then** cada tarefa apresentada tem exatamente esse estado.
3. **Given** a lista de tarefas de um projeto e um responsável selecionado, **When** aplica o filtro de responsável, **Then** cada tarefa apresentada está atribuída a esse responsável.
4. **Given** nenhum resultado correspondente ao filtro escolhido, **When** o filtro é aplicado, **Then** a lista não apresenta tarefas e indica que não existem resultados.

## Casos excecionais relevantes

1. **Credenciais inválidas:** negar acesso e não revelar se o email está registado.
2. **Acesso indevido:** utilizadores sem associação ao projeto não podem consultar nem alterar o projeto, as tarefas ou o resumo, incluindo através de acesso direto.
3. **Atribuição não elegível:** impedir atribuição a alguém que não esteja associado ao projeto e preservar o responsável atual.
4. **Campos obrigatórios em falta:** recusar a gravação e não criar registos incompletos.
5. **Projeto sem tarefas:** mostrar totais iguais a zero e uma lista em aberto vazia.
6. **Atualizações concorrentes:** não existe regra definida para duas pessoas alterarem a mesma tarefa antes de qualquer delas guardar; decidir como prevenir perda silenciosa de alterações.

## Questões por confirmar

- Confirmar permissões por papel, alcance do Admin e possibilidade de acumular papéis.
- Definir como criar, convidar, desativar e remover utilizadores. US-08 cobre apenas utilizadores existentes; o mecanismo de disponibilização das primeiras contas é um bloqueio em aberto.
- Confirmar regras propostas: título obrigatório e descrição opcional para projetos; título e estado obrigatórios, descrição e responsável opcionais para tarefas.
- Confirmar se uma tarefa pode ter vários responsáveis; a proposta atual suporta zero ou um.
- Confirmar nomes e transições dos estados e validar que “em aberto” significa estado diferente de “Concluída”.
- Definir comportamento de projeto arquivado; o arquivamento foi retirado do MVP até confirmação.
- Definir como remover membros e o que fazer às tarefas que lhes estão atribuídas.
- Definir como evitar que a alteração de papéis deixe a equipa sem um Admin.
- Definir resultado verificável para falhas de gravação e alterações simultâneas.
- Definir limites de tamanho dos campos para que a validação de conteúdo fique totalmente objetiva.
