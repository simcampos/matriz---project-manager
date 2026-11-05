# Verificação do MVP

Data da verificação: 2026-11-04

## Testes automatizados

### Testes pedidos

- **Comando:** `cd backend && ../.venv/bin/python manage.py check && ../.venv/bin/python manage.py test`
- **Resultado esperado:** verificação Django sem problemas e testes de validação de tarefas, autorização de projetos e criação/consulta de tarefas aprovados.
- **Resultado observado:** `manage.py check` sem problemas; 39 testes passaram.
- **Evidência:** `Ran 39 tests ... OK`. A suite inclui:
  - `test_title_and_description_constraints_are_validated` em `backend/apps/tasks/tests.py` (título vazio e só espaços devolvem 400).
  - `test_inaccessible_and_missing_projects_return_not_found` em `backend/apps/projects/tests.py` (utilizador sem acesso recebe 404).
  - `test_create_defaults_and_returns_a_retrievable_task` em `backend/apps/tasks/tests.py` (POST 201 e GET 200 com os dados persistidos).
- **Estado:** PASS

### Regressão da verificação de sessão anónima

- **Comando:** `cd frontend && npm test`
- **Resultado esperado:** a consulta de sessão sem autenticação não deve ser tratada como uma sessão expirada; pedidos protegidos continuam a emitir o evento de sessão expirada e falhas de login não o emitem.
- **Resultado observado:** 3 testes passaram.
- **Evidência:** `node --test test/sessionExpired.test.js`; 3 pass, 0 fail.
- **Estado:** PASS

### Build e higiene do diff

- **Comando:** `cd frontend && npm run build`
- **Resultado esperado:** build de produção concluído sem erros.
- **Resultado observado:** build Vite concluído; 20 módulos transformados.
- **Evidência:** saída `✓ built`.
- **Estado:** PASS

- **Comando:** `git diff --check`
- **Resultado esperado:** nenhuma falha de whitespace.
- **Resultado observado:** comando terminou com código 0 e sem output.
- **Evidência:** saída vazia, código de saída 0.
- **Estado:** PASS

## Casos manuais

Os passos foram executados no frontend local e, quando indicado, diretamente na API. Foram usados utilizadores e recursos temporários; todos foram removidos no fim da verificação.

### Caso: 01 — Acesso à aplicação

- **Passos:** abrir a aplicação sem sessão; consultar `GET /api/users/me/`; tentar login com palavra-passe inválida e depois com credenciais temporárias válidas.
- **Resultado esperado:** sem sessão, apresentar login sem conteúdo protegido; credenciais inválidas não autenticam; credenciais válidas abrem o painel.
- **Resultado observado:** `/api/users/me/` devolveu 401; o login inválido apresentou “Email ou palavra-passe inválidos.”; o login válido abriu o painel. Após a correção descrita abaixo, a entrada anónima não apresenta alerta de sessão expirada.
- **Evidência:** respostas HTTP 401 e estado do browser; `/api/health/` devolveu 200 e `/api/csrf/` devolveu 204.
- **Estado:** PASS

### Caso: 02 — Gestão de projetos

- **Passos:** criar um projeto pela interface; pesquisá-lo; editar o título; eliminá-lo e confirmar a ação.
- **Resultado esperado:** o projeto criado aparece sem recarregar, a pesquisa encontra o projeto, a edição persiste e a eliminação remove-o.
- **Resultado observado:** criação, pesquisa e edição foram refletidas na interface; a confirmação de eliminação regressou ao painel sem projetos. Depois, GET ao projeto devolveu 404 e a pesquisa devolveu uma lista vazia.
- **Evidência:** estado do browser; `GET /api/projects/7/` → 404; `GET /api/projects/?name=...` → 200 com `[]`.
- **Estado:** PASS

### Caso: 03 — Persistência de tarefas

- **Passos:** criar uma tarefa; confirmar a listagem e a contagem; recarregar a aplicação; reiniciar o backend; voltar a autenticar e abrir o projeto e a tarefa.
- **Resultado esperado:** a tarefa e os seus dados mantêm-se após recarregar e reiniciar o backend.
- **Resultado observado:** a tarefa apareceu imediatamente; depois do reload e do reinício do backend, continuavam visíveis a tarefa, o estado `IN_PROGRESS`, o responsável e o comentário. O painel mostrou uma tarefa em progresso.
- **Evidência:** browser antes/depois do reload e do restart; `GET /api/health/` após o restart devolveu `{"status":"ok","database":"ok"}`.
- **Estado:** PASS

### Caso: 04 — Validação de dados

- **Passos:** submeter tarefa com título só de espaços na interface; enviar pela API títulos vazio e só de espaços, bem como estado `BLOCKED`; submeter comentário só de espaços.
- **Resultado esperado:** os dados inválidos são rejeitados com erro, sem criar registos.
- **Resultado observado:** título vazio, título só de espaços, estado inválido e comentário só de espaços devolveram 400. A interface apresentou mensagens de validação para título e comentário.
- **Evidência:** respostas HTTP 400; para estado inválido, corpo `{"status":["\"BLOCKED\" não é um escolha válido."]}`; não foi criada tarefa ou comentário a partir das submissões inválidas.
- **Estado:** PASS

### Caso: 05 — Estado, filtros e contagens

- **Passos:** alterar o estado da tarefa de `TODO` para `IN_PROGRESS`; filtrar por esse estado e pela prioridade `MEDIUM`; recarregar o painel.
- **Resultado esperado:** a tarefa aparece no filtro correspondente e as contagens do projeto e do painel são atualizadas.
- **Resultado observado:** a contagem passou de 1 “Por fazer” para 1 “Em progresso”; o filtro combinado apresentou a tarefa; após reload o painel continuou a mostrar 1 tarefa em progresso.
- **Evidência:** estado do browser e contagens visíveis antes/depois da alteração.
- **Estado:** PASS

### Caso: 06 — Responsáveis

- **Passos:** atribuir o gestor do projeto; tentar repetir a atribuição diretamente na API; remover a atribuição pela interface e confirmar a lista atualizada.
- **Resultado esperado:** a atribuição aparece uma vez, repetição é recusada e a remoção atualiza a lista sem recarregar.
- **Resultado observado:** a interface confirmou a atribuição; a repetição devolveu 409; a lista não duplicou o utilizador; a remoção apresentou feedback e deixou a lista vazia.
- **Evidência:** `POST /api/projects/7/tasks/7/assignees/` duplicado → 409; interface mostrou “Responsável atribuído.” e “Responsável removido.”.
- **Estado:** PASS

### Caso: 07 — Comentários

- **Passos:** adicionar comentário pela interface; consultar a tarefa; recarregar e reiniciar o backend; voltar a abrir a tarefa.
- **Resultado esperado:** o comentário aparece com autor autenticado e data definida pelo backend e mantém-se persistido.
- **Resultado observado:** o comentário apareceu com o utilizador autenticado e data/hora; continuou visível após reload e restart.
- **Evidência:** item de comentário na interface com autor, `<time>` e conteúdo; comentário voltou a aparecer após reinício do backend.
- **Estado:** PASS

### Caso: 08 — Autorização na API

- **Passos:** autenticar um segundo utilizador sem associação ao projeto; consultar projeto, lista/detalhe de tarefas, responsáveis e comentários; tentar alterar projeto e tarefa.
- **Resultado esperado:** recursos inacessíveis não são revelados nem alterados.
- **Resultado observado:** os cinco GETs e os dois PATCHs devolveram 404; o painel do segundo utilizador não apresentou projetos.
- **Evidência:** HTTP 404 para `/projects/7/`, `/projects/7/tasks/`, `/projects/7/tasks/7/`, `/assignees/`, `/comments/` e para PATCH de projeto e tarefa.
- **Estado:** PASS

### Caso: 09 — Eliminação e erros

- **Passos:** eliminar a tarefa e confirmar; eliminar o projeto e confirmar; consultar os recursos removidos; simular falha de rede ao submeter um projeto e voltar a consultar os resultados.
- **Resultado esperado:** eliminações confirmadas atualizam a interface e removem recursos dependentes; uma falha não é apresentada como sucesso e preserva os campos do formulário.
- **Resultado observado:** a tarefa desapareceu e as contagens ficaram a zero; o diálogo do projeto informou que tarefas, responsáveis e comentários dependentes seriam eliminados. Após eliminar, GETs devolveram 404 e a pesquisa ficou vazia. A falha de rede apresentou mensagem de erro, manteve título e descrição no formulário e não criou projeto.
- **Evidência:** diálogos de confirmação; GET ao projeto/tarefa → 404; pesquisa → `[]`; pedido POST abortado no browser e valores do formulário confirmados após a falha.
- **Estado:** PASS

## Bug encontrado e correção

- **Reprodução:** abrir/recarregar a aplicação sem sessão autenticada.
- **Resultado observado antes da correção:** a consulta inicial `GET /api/users/me/` devolvia 401 e o formulário de login mostrava “A sessão terminou ou não é válida. Inicia sessão novamente.” apesar de não ter existido sessão autenticada nessa visita.
- **Evidência:** resposta 401 da API e alerta visível no browser; endpoints de health e CSRF respondiam normalmente, excluindo falha de conectividade.
- **Conclusão:** `apiRequest` emitia o evento de sessão expirada para qualquer 401, incluindo a verificação inicial esperada em `/users/me/`; o listener apresentava o alerta. Não ficou hipótese pendente para esta causa.
- **Correção limitada:** a verificação inicial `/users/me/` já não emite o evento; a aplicação define explicitamente o estado anónimo para esse 401. Pedidos protegidos continuam a emitir o evento.
- **Regressão:** `frontend/test/sessionExpired.test.js` verifica a consulta inicial, pedidos protegidos e falhas de login; os 3 testes passaram. Após a correção, abrir a aplicação anónima mostrou o formulário sem o alerta indevido.

## Exemplos de utilização da IA

### Exemplo 1 — Diagnóstico do alerta na entrada anónima

- **Objetivo do pedido à IA:** investigar por que motivo abrir a aplicação sem sessão mostrava um alerta de sessão expirada.
- **Decisão do programador:** aceitar a correção limitada à consulta inicial de `/users/me/`; manter o evento de sessão expirada para pedidos protegidos.
- **Verificação:** reproduzir a resposta 401 sem alerta no browser e executar `cd frontend && npm test`. Resultado observado: 3 testes passaram, cobrindo a consulta inicial, pedidos protegidos e falhas de login.

### Exemplo 2 — Refatoração de validação partilhada

- **Objetivo do pedido à IA:** identificar uma refatoração de baixo risco para remover duplicação na validação de campos desconhecidos.
- **Decisão do programador:** aceitar centralizar `StrictSerializer` em `backend/apps/common/serializers.py`, mas manter a alteração num commit separado da implementação funcional.
- **Verificação:** executar `manage.py check`, a suite backend (39 testes), os testes frontend (3 testes), `npm run build` e `git diff --check`. Todos passaram após a refatoração.

### Exemplo 3 — Operações previstas no contrato mas ausentes

- **Objetivo do pedido à IA:** comparar o OpenAPI com as rotas reais e identificar operações que não estavam implementadas.
- **Sugestão da IA e decisão do programador:** foi sugerido completar a gestão de papéis e membros. O programador aceitou implementar RF-03 e RF-05 e definiu que o Admin tem leitura global sem escrita/comentários, que podem ser associados utilizadores ativos de qualquer papel, que remover um membro remove as suas atribuições e que deve permanecer pelo menos um Admin ativo.
- **Verificação:** executar os testes de backend e frontend, compilar o frontend e validar o OpenAPI. Os resultados desta implementação estão registados abaixo.

## Verificação adicional — Admin e membros de projeto

Data da verificação: 2026-11-05

### Testes automatizados

- **Comando:** `cd backend && ../.venv/bin/python manage.py check && ../.venv/bin/python manage.py test apps.accounts apps.projects apps.tasks apps.comments`
- **Resultado esperado:** verificações Django sem problemas e suite backend aprovada, incluindo permissões de Admin, proteção do último Admin ativo, gestão de membros, limpeza de atribuições e bloqueio de comentário por Admin.
- **Resultado observado:** `manage.py check` sem problemas; 48 testes passaram.
- **Evidência:** `Ran 48 tests ... OK`. Casos relevantes incluem `test_last_active_admin_cannot_be_demoted`, `test_admin_can_read_projects_without_managing_them`, `test_project_manager_can_add_and_remove_members_and_assignments`, `test_only_project_manager_can_manage_members` e `test_admin_can_read_comments_but_cannot_add_them`.
- **Estado:** PASS

- **Comando:** `cd frontend && npm test && npm run build`
- **Resultado esperado:** testes de frontend aprovados e bundle de produção compilado.
- **Resultado observado:** 3 testes passaram; build Vite concluído com 22 módulos transformados.
- **Evidência:** `3 pass, 0 fail`; `✓ built`.
- **Estado:** PASS

- **Comando:** `ruby -e 'require "yaml"; root = YAML.load_file("openapi.yaml"); refs = []; walk = ->(value) { case value; when Hash; value.each { |key, child| refs << child if key == "$ref"; walk.call(child) }; when Array; value.each { |child| walk.call(child) }; end }; walk.call(root); refs.each { |ref| next unless ref.start_with?("#/"); cursor = root; ref.split("/").drop(1).each { |part| cursor = cursor.fetch(part.gsub("~1", "/").gsub("~0", "~")) } }; puts "OpenAPI YAML valid; #{root.fetch("paths").length} paths; #{refs.length} local references resolved"'`
- **Resultado esperado:** contrato OpenAPI sintaticamente válido.
- **Resultado observado:** YAML válido; 17 caminhos e 134 referências locais resolvidos.
- **Evidência:** parser Ruby `Psych` terminou com código 0 e imprimiu `OpenAPI YAML valid; 17 paths; 134 local references resolved`.
- **Estado:** PASS

- **Comando:** `git diff --check`
- **Resultado esperado:** nenhuma falha de whitespace no conjunto de alterações.
- **Resultado observado:** terminou com código 0 e sem output.
- **Evidência:** saída vazia; código de saída 0.
- **Estado:** PASS

### Verificações manuais

- **Admin em modo de consulta:** não executado manualmente no browser nesta sessão. Os testes automatizados verificam leitura global e que o Admin não consegue alterar os dados nem adicionar comentários; a verificação interativa da interface fica pendente porque a ferramenta de browser não está disponível nesta sessão.
- **Gestão de membros:** não executado manualmente no browser nesta sessão. Os testes automatizados verificam associação/remoção, limpeza das atribuições, acesso após remoção e restrição de gestão ao Project Manager responsável.
