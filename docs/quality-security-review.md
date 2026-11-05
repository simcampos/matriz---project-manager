# Revisão de qualidade e segurança — Exercício 5

**Data:** 2026-11-05
**Commit do incremento revisto:** [a5d53cac7fb94ea3e69858ae742da5695274746a](https://github.com/simcampos/matriz---project-manager/commit/a5d53cac7fb94ea3e69858ae742da5695274746a)

O incremento contém testes de validação e persistência de tarefas, um fluxo E2E e a respetiva configuração/documentação. Não altera código de produção.

## 1. Code Review

Não foram registados findings `CR-xx` no incremento revisto.

| ID | Ficheiro | Problema | Severidade | Estado (Corrigido/Pendente/Rejeitado) | Decisão humana |
|---|---|---|---|---|---|

A Fase 1 foi apresentada sem findings. Não houve decisões individuais de aceitar, rejeitar ou corrigir.

## 2. Security Review

A revisão estática não identificou vulnerabilidades confirmadas ou suspeitas nas áreas analisadas. A tabela não contém findings `SEC-xx`.

| ID | Tipo | Ficheiro | Severidade | Estado (Confirmado/Suspeita/Por validar) |
|---|---|---|---|---|

**Verificação manual com duas contas:** não executada; permanece **por validar**. Os passos propostos foram criar um projeto novo como `pm@matriz.dev`, não associar `developer@matriz.dev` e, numa sessão separada, tentar consultar e alterar o projeto e a tarefa. Espera-se `404` para recursos inacessíveis e ausência de alterações. O Developer do seed pode já pertencer a outros projetos, pelo que o teste deve usar um projeto novo.

A Fase 2 foi autorizada pelo utilizador. Como não houve findings, não foi necessária uma decisão de aceitar ou rejeitar vulnerabilidades nem foram propostas correções.

## 3. Correções Aplicadas

Não foram implementadas correções de produção decorrentes da revisão; não há commit de correção a referenciar.

O commit [a5d53cac7fb94ea3e69858ae742da5695274746a](https://github.com/simcampos/matriz---project-manager/commit/a5d53cac7fb94ea3e69858ae742da5695274746a) acrescenta cobertura de testes — não é uma correção:

- Validação de títulos, valores inválidos, filtros, persistência e autorização de tarefas em `backend/apps/tasks/tests.py`.
- Fluxo de criação de projeto e tarefa pela interface em `frontend/e2e/task-flow.spec.js`.

## 4. Problemas Pendentes

- Não há findings `CR-xx` ou `SEC-xx` por corrigir.
- A verificação manual de controlo de acesso com duas contas continua pendente; é uma validação não executada, não uma vulnerabilidade identificada.
- A configuração de produção e os logs de infraestrutura não foram verificados.

## 5. Verificações Executadas vs. Por Validar

### Executadas

- `manage.py check`: sem problemas.
- Backend (`apps.accounts`, `apps.projects`, `apps.tasks`, `apps.comments`): 61 testes passaram.
- Frontend (`npm test`): 3 testes passaram.
- Build frontend (`npm run build`): passou.
- Playwright E2E com o Chrome instalado no sistema: 1 teste passou; o projeto de teste foi eliminado no teardown.
- Compose E2E: configuração validada. A base E2E não tinha migrations pendentes; o seed não criou registos.
- `git diff --check`: sem problemas.

### Por validar

- Teste manual de IDOR/autorização com Project Manager e Developer, incluindo tentativas de alteração e confirmação de que os dados permanecem inalterados.
- Configuração efetiva de produção e logging fora da aplicação.

O teste manual não foi executado porque a revisão foi estática e a validação posterior cobriu as suites automatizadas; não se deve interpretar a sua ausência como confirmação do comportamento em runtime.
