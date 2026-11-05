# Plano de testes do MVP — tarefas e autorização

## Objetivo e âmbito

Este documento define cenários de teste derivados dos requisitos, critérios de aceitação e contrato OpenAPI do MVP. Não descreve o comportamento observado na implementação e não implementa nem executa testes.

Âmbito:

- Validação de título, descrição, estado e prioridade das tarefas.
- Criação e consulta de tarefas pela API.
- Recusa de acesso a tarefas de projetos aos quais o utilizador não está associado.

Stack relevante: Python, Django, Django REST Framework, PostgreSQL, React e Vite. Os testes de integração da API usam o test runner do Django e o cliente de testes da DRF. O teste E2E da interface usa Playwright e cobre o fluxo descrito na secção de execução E2E.

## Princípios de execução

- Cada cenário deve preparar os seus próprios dados e poder correr isoladamente, sem depender de outro cenário.
- Os testes de API devem verificar a resposta HTTP e, quando aplicável, o estado persistido. Uma falha de validação não pode criar a tarefa; uma tentativa de atualização recusada não pode alterar os valores existentes.
- Nos cenários de acesso negado, o utilizador deve estar autenticado, não ser Admin e não estar associado ao projeto da tarefa. A tarefa deve pertencer a um projeto distinto, previamente criado para o cenário.
- Quando um cenário enumera vários valores, cada valor deve ser executado como caso independente, por exemplo, com parametrização.
- Os códigos de erro e os campos de resposta devem respeitar o contrato OpenAPI. Este define erros de validação `400`, autenticação ausente/inválida `401`, falta de permissão `403` e recurso inexistente ou não acessível `404`.

## Matriz de cenários

### Cenários positivos

| ID | Prioridade | Descrição | Pré-condições | Entrada / ação | Resultado esperado | Nível |
|---|---|---|---|---|---|---|
| TC-01 | P1 | Aceitar título no limite mínimo | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título de exatamente 3 caracteres não brancos | `201`; tarefa associada ao projeto e título aceite | Integração |
| TC-02 | P1 | Aceitar título no limite máximo | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título de exatamente 150 caracteres | `201`; tarefa criada | Integração |
| TC-03 | P1 | Aceitar descrição no limite máximo | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com descrição de exatamente 2000 caracteres | `201`; descrição aceite | Integração |
| TC-04 | P1 | Criar tarefa sem descrição | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título válido e sem o campo `description` | `201`; tarefa criada; a resposta respeita o esquema `Task` | Integração |
| TC-05 | P1 | Aceitar estados permitidos | PM autenticado com permissão para criar tarefas num projeto | Criar uma tarefa por execução com `TODO`, `IN_PROGRESS` ou `DONE` | `201`; a tarefa devolve o estado enviado | Integração |
| TC-06 | P1 | Aceitar prioridades permitidas | PM autenticado com permissão para criar tarefas num projeto | Criar uma tarefa por execução com `LOW`, `MEDIUM` ou `HIGH` | `201`; a tarefa devolve a prioridade enviada | Integração |
| TC-07 | P1 — condicionado | Aplicar defaults ao omitir estado e prioridade | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título válido, sem `status` nem `priority` | Se a omissão for confirmada: `201`, estado `TODO` e prioridade `MEDIUM` | Integração |
| TC-08 | P0 | Criar tarefa com sucesso pela API | PM autenticado com permissão de gestão sobre o projeto | `POST /projects/{projectId}/tasks/` com título válido e valores permitidos | `201`; resposta identifica a tarefa e o projeto, devolve os valores aceites e inclui `Location` | Integração |
| TC-09 | P0 | Consultar lista de tarefas com sucesso | Utilizador com acesso ao projeto; tarefa desse projeto previamente criada | `GET /projects/{projectId}/tasks/` | `200`; lista inclui a tarefa esperada e apenas tarefas do projeto | Integração |
| TC-10 | P0 | Consultar tarefa individual com sucesso | Utilizador com acesso ao projeto; tarefa previamente criada | `GET /projects/{projectId}/tasks/{taskId}/` | `200`; resposta identifica a tarefa e devolve os seus valores | Integração |

### Cenários negativos

| ID | Prioridade | Descrição | Pré-condições | Entrada / ação | Resultado esperado | Nível |
|---|---|---|---|---|---|---|
| TC-11 | P0 | Rejeitar título vazio na criação | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com `title: ""` | `400`, erro de validação de título e tarefa não criada | Integração |
| TC-12 | P0 | Rejeitar título composto só por espaços na criação | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título formado apenas por espaços | `400`, erro de validação de título e tarefa não criada | Integração |
| TC-13 | P0 | Rejeitar título abaixo do limite na criação | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título de 2 caracteres | `400` e tarefa não criada | Integração |
| TC-14 | P0 | Rejeitar título acima do limite na criação | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título de 151 caracteres | `400` e tarefa não criada | Integração |
| TC-15 | P1 | Rejeitar descrição acima do limite na criação | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com descrição de 2001 caracteres | `400` e tarefa não criada | Integração |
| TC-16 | P1 | Rejeitar estado não permitido | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com `status: "BLOCKED"` | `400`, erro de validação de estado e tarefa não criada | Integração |
| TC-17 | P1 | Rejeitar prioridade não permitida | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com `priority: "URGENT"` | `400`, erro de validação de prioridade e tarefa não criada | Integração |
| TC-18 | P1 | Preservar tarefa após atualização inválida do título | PM autenticado com permissão para editar; tarefa com título conhecido | Enviar `PATCH` com título vazio, só espaços, de 2 ou de 151 caracteres; executar cada valor separadamente | `400`; título persistido permanece igual ao anterior | Integração |
| TC-19 | P1 | Preservar tarefa após atualização inválida do estado | PM autenticado com permissão para editar; tarefa com estado conhecido | Enviar `PATCH` com `status: "BLOCKED"` | `400`; estado persistido permanece igual ao anterior | Integração |
| TC-20 | P1 | Preservar tarefa após atualização inválida da prioridade | PM autenticado com permissão para editar; tarefa com prioridade conhecida | Enviar `PATCH` com `priority: "URGENT"` | `400`; prioridade persistida permanece igual à anterior | Integração |
| TC-21 | P1 | Preservar tarefa após atualização inválida da descrição | PM autenticado com permissão para editar; tarefa com descrição conhecida | Enviar `PATCH` com descrição de 2001 caracteres | `400`; descrição persistida permanece igual à anterior | Integração |
| TC-22 | P0 | Impedir consulta direta por utilizador sem acesso ao projeto | Developer autenticado, não Admin e não associado ao projeto da tarefa | `GET /projects/{projectId}/tasks/{taskId}/` | `404`; conteúdo da tarefa não é apresentado | Integração |
| TC-23 | P1 — código por confirmar | Impedir alteração por utilizador sem acesso ao projeto | Developer autenticado, não Admin e não associado ao projeto; tarefa com estado conhecido | Enviar `PATCH` da tarefa com alteração de estado | Pedido recusado; estado persistido não muda. O código esperado (`403` ou `404`) depende de confirmação da regra de resposta | Integração |

### Edge cases e limites

| ID | Prioridade | Descrição | Pré-condições | Entrada / ação | Resultado esperado | Nível |
|---|---|---|---|---|---|---|
| TC-24 | P2 — semântica por confirmar | Enviar descrição explicitamente nula | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com `description: null` | O OpenAPI permite `null`; confirmar se o comportamento esperado é equivalente a omitir a descrição e qual o valor devolvido na resposta | Integração |
| TC-25 | P2 — semântica por confirmar | Enviar descrição vazia ou só com espaços | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com `description: ""` e, em execução separada, só espaços | A documentação não define mínimo nem proíbe espaços na descrição; definir o resultado esperado antes de fixar o teste | Integração |
| TC-26 | P2 — normalização por confirmar | Verificar espaços externos no título | PM autenticado com permissão para criar tarefas num projeto | Criar tarefa com título que tenha espaços externos e cujo conteúdo após remoção tenha 3–150 caracteres | Validar o limite pelo conteúdo sem espaços externos; confirmar se o título devolvido deve ser normalizado ou preservar o valor enviado | Integração |

## Prioridades

- **P0 — essenciais:** TC-11 a TC-14 (título inválido), TC-08 (criação), TC-09 e TC-10 (consulta), TC-22 (consulta não autorizada).
- **P1 — cobertura funcional adicional:** limites válidos, descrição, valores de estado/prioridade, erros de enumeração e preservação dos dados em atualizações inválidas.
- **P2 — dependem de clarificação:** tratamento de descrição nula/vazia e normalização de espaços no título.

## Pressupostos, divergências e decisões pendentes

Esta secção distingue o que está descrito nos documentos dos pontos que ainda não devem ser tratados como decisões aprovadas.

### Critérios usados para os casos

- A US-04 e o OpenAPI definem título com 3–150 caracteres, não composto apenas por espaços; descrição opcional até 2000 caracteres; estados `TODO`, `IN_PROGRESS`, `DONE`; prioridades `LOW`, `MEDIUM`, `HIGH`.
- O OpenAPI permite omitir `status` e `priority` na criação e documenta os defaults `TODO` e `MEDIUM`. A US-04 também diz que os valores omitidos assumem esses defaults.
- A consulta de tarefa não acessível é documentada no OpenAPI como `404` para recurso inexistente ou não acessível.
- Os cenários de autorização usam um utilizador sem associação ao projeto, não simplesmente um utilizador que não esteja atribuído à tarefa. O Admin é excluído dos cenários negativos, pois pode consultar tarefas de todos os projetos.

### Confirmações necessárias

1. **Estado obrigatório ou opcional na criação:** `constraints.md` descreve tarefa com estado obrigatório, em conflito com a US-04 e o OpenAPI, que permitem omiti-lo e indicam o default `TODO`. TC-07 é condicionado até esta divergência ser resolvida.
2. **Código de resposta ao atualizar recurso inacessível:** o OpenAPI lista `403` e `404` para `PATCH`, mas não fixa qual se aplica a um utilizador sem associação ao projeto. TC-23 verifica a recusa e a ausência de alteração; confirmar o código HTTP antes de o tornar uma asserção fixa.
3. **Descrição nula, vazia ou só com espaços:** o OpenAPI permite `null` e não estabelece mínimo para a string; os critérios dizem apenas que a descrição é opcional e limitada a 2000 caracteres. Confirmar se `null`, string vazia e espaços são equivalentes ou têm tratamento distinto.
4. **Normalização do título:** a US-04 especifica que o limite é considerado depois de remover espaços externos, mas não estabelece se o valor guardado/devolvido deve também ser aparado. Não verificar a normalização até esta regra ser confirmada.
5. **Autorização de escrita:** a US-04 exige que utilizador sem associação não consiga alterar a tarefa. O plano verifica que o valor não muda e deixa o código HTTP em aberto conforme o contrato disponível.

## Execução dos testes unitários de título

Implementados em `backend/apps/tasks/tests.py`, na classe `TaskTitleValidationTests`, usando `TaskCreateSerializer` diretamente e `SimpleTestCase`. Cada teste tem um único assert principal e não acede à base de dados.

| Teste | Descrição | Input | Resultado esperado | Resultado obtido |
|---|---|---|---|---|
| `test_valid_title_is_accepted` | Aceitar título válido | `"Implementar login"` | Título aceite | Passou |
| `test_empty_title_is_rejected_with_blank_message` | Rejeitar título vazio e verificar mensagem | `""` | Erro de campo: “Este campo não pode ser em branco.” | Passou |
| `test_whitespace_only_title_is_rejected` | Rejeitar título só com espaços | `"   "` | Erro de validação `blank` | Passou |
| `test_two_character_title_is_rejected` | Rejeitar título abaixo do mínimo | `"ab"` | Erro de validação `min_length` | Passou |
| `test_three_character_title_is_accepted` | Aceitar o limite mínimo | `"abc"` | Título aceite | Passou |
| `test_150_character_title_is_accepted` | Aceitar o limite máximo | `"x" * 150` | Título aceite | Passou |
| `test_151_character_title_is_rejected` | Rejeitar título acima do máximo | `"x" * 151` | Erro de validação `max_length` | Passou |

Execução final dos sete testes: `.venv/bin/python backend/manage.py test apps.tasks.tests.TaskTitleValidationTests -v 2` — 7 testes passaram.

Verificação da suite completa da aplicação de tarefas: `.venv/bin/python backend/manage.py test apps.tasks -v 2` — 23 testes passaram; system check sem problemas.

Na primeira execução do teste do título vazio, a expectativa usava a mensagem inglesa padrão, mas a aplicação devolveu a mensagem localizada em português. O teste foi corrigido para esperar a mensagem observada; não foi alterado código de produção. Após a correção, os sete testes unitários e a suite completa de tarefas passaram.

## Execução dos testes de integração da API e persistência

Implementados em `backend/apps/tasks/tests.py`, na classe `TaskPersistenceIntegrationTests`, com `django.test.TestCase` e `rest_framework.test.APIClient(enforce_csrf_checks=True)`. A autenticação usa o endpoint de sessão e cookie de sessão; os pedidos `POST` usam o token CSRF obtido em `/api/csrf/`. Cada teste cria os seus próprios utilizadores e projeto através da API. O test runner criou a base PostgreSQL isolada `test_matriz`; `TestCase` reverte os dados de cada teste e o runner remove a base de teste ao terminar.

Todos os pedidos JSON usam `Content-Type: application/json`. Nos `POST`, o cliente envia também `X-CSRFToken` e o cookie CSRF; após autenticação, os pedidos usam o cookie de sessão. Os valores de credenciais são fixtures sintéticas locais, não credenciais reais.

| Teste | Pré-condições e setup | Request enviado | Resultado esperado | Resultado obtido / estado |
|---|---|---|---|---|
| `test_api_creation_persistence_and_retrieval` | Utilizador Project Manager de teste autenticado por sessão; projeto criado por `POST /api/projects/` com `{"title":"Integration project"}` | `POST /api/projects/{projectId}/tasks/` com `{"title":"Persisted integration task","description":"Created through the API"}`; depois `GET /api/projects/{projectId}/tasks/{taskId}/` | `POST` `201`, ID positivo, campos correspondentes, estado `TODO` e prioridade `MEDIUM`; registo persistido; `GET` `200` com a mesma representação | PASS — resposta e registo persistido confirmados; GET devolveu os mesmos dados |
| `test_empty_title_returns_validation_error` | Novo Project Manager autenticado e projeto criado pela API | `POST /api/projects/{projectId}/tasks/` com `{"title":""}` | `400`, erro no campo `title` e nenhuma tarefa criada | PASS — `400`, erro presente e nenhuma tarefa no projeto |
| `test_whitespace_only_title_returns_validation_error` | Novo Project Manager autenticado e projeto criado pela API | `POST /api/projects/{projectId}/tasks/` com `{"title":"   "}` | `400`, erro no campo `title` e nenhuma tarefa criada | PASS — `400`, erro presente e nenhuma tarefa no projeto |
| `test_title_below_minimum_returns_validation_error` | Novo Project Manager autenticado e projeto criado pela API | `POST /api/projects/{projectId}/tasks/` com `{"title":"ab"}` | `400`, erro no campo `title` e nenhuma tarefa criada | PASS — `400`, erro presente e nenhuma tarefa no projeto |
| `test_user_without_project_access_gets_not_found` | Project Manager autenticado cria projeto e tarefa pela API; utilizador Developer B autentica-se sem associação ao projeto | Como B: `GET /api/projects/{projectId}/tasks/{taskId}/` | `404`; conteúdo da tarefa não é revelado | PASS — `404`; título da tarefa ausente da resposta |
| `test_nonexistent_task_id_returns_not_found` | Project Manager autenticado e projeto criado pela API; ID inteiro positivo sem tarefa correspondente | `GET /api/projects/{projectId}/tasks/{taskId}/` | `404` | PASS — `404` |

Execução direcionada: `.venv/bin/python backend/manage.py test apps.tasks.tests.TaskPersistenceIntegrationTests -v 2` — 6 testes passaram.

Suite completa: `.venv/bin/python backend/manage.py test apps.tasks -v 2` — 29 testes passaram; system check sem problemas.

## Execução E2E do fluxo de utilizador

Implementado em `frontend/e2e/task-flow.spec.js` com Playwright. O teste usa locators por roles e labels acessíveis, sem seletores de classes CSS nem esperas temporizadas. Cria o seu próprio projeto via UI com título único, cria uma tarefa e elimina o projeto (e a tarefa em cascata) num `afterEach` autenticado com CSRF.

O ambiente usa Playwright Chromium contra Google Chrome instalado localmente através de `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, frontend em `http://127.0.0.1:5174`, backend em `http://127.0.0.1:8001` e o serviço PostgreSQL isolado `matriz_e2e` na porta `5433`. A conta Project Manager foi criada pelo seed apenas nessa base E2E. Não foi usada a base de desenvolvimento.

Comando executado: `cd frontend && PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" npm run test:e2e`.

Resultado: `1 passed (5.8s)`. A criação do projeto e da tarefa devolveu `201`; o estado apresentado foi `TODO`; o teardown eliminou o projeto com `204`. Não foram gerados screenshot nem trace porque não houve falha. Os logs dos servidores registaram login `200`, operações de leitura `200`, criação do projeto/tarefa `201` e limpeza `204`.

## Referências

- [Requisitos do MVP](./requirements.md)
- [User Stories e critérios de aceitação](./user-stories.md)
- [Restrições, pressupostos e decisões pendentes](./constraints.md)
- [Contrato OpenAPI](../openapi.yaml)
