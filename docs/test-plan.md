# Plano e resultados de testes — Matriz

**Atualizado:** 2026-11-05
**Incremento testado:** [a5d53cac7fb94ea3e69858ae742da5695274746a](https://github.com/simcampos/matriz---project-manager/commit/a5d53cac7fb94ea3e69858ae742da5695274746a)

## 1. Âmbito

Os cenários TC-01 a TC-26 abaixo foram preservados do plano existente no repositório, que detalha os critérios de tarefas e autorização. A lista específica de cenários do Exercício 1 e os outputs originais dos Exercícios 2–4 não foram incluídos no pedido; os resultados registados nesta versão limitam-se às execuções observadas durante esta revisão.

Esta fase cobre:

- Validação de títulos, descrição, estado e prioridade das tarefas.
- Criação, listagem, consulta, atualização e eliminação de tarefas pela API.
- Persistência, filtros e autorização de tarefas.
- Testes frontend de expiração de sessão, build e um fluxo E2E de criação por Project Manager.

Os resultados da coluna **Resultado Obtido** distinguem testes executados de cenários ainda por validar. Os resultados esperados são critérios do plano/requisitos e não constituem, por si só, evidência de execução.

## 2. Cenários de Teste

| ID | Descrição | Nível | Pré-condições | Input | Resultado Esperado | Resultado Obtido | Estado |
|---|---|---|---|---|---|---|---|
| TC-01 | Aceitar título no limite mínimo | Unitário | Serializer de criação | `title: "abc"` | Título aceite | Serializer aceitou o título. | Passou |
| TC-02 | Aceitar título no limite máximo | Unitário | Serializer de criação | Título com 150 caracteres | Título aceite | Serializer aceitou o título. | Passou |
| TC-03 | Aceitar descrição no limite máximo | Integração | PM com permissão de gestão | Descrição com 2000 caracteres | `201`; descrição aceite | Não foi executado um caso de exatamente 2000 caracteres. | Por validar |
| TC-04 | Criar tarefa sem descrição | Integração | PM com permissão de gestão | POST com título válido e campo `description` omitido | `201`; tarefa criada | O teste API usou `description: null`; não verificou a omissão do campo. | Por validar |
| TC-05 | Aceitar estados permitidos | Integração | Tarefa acessível ao PM/Developer atribuído | `TODO`, `IN_PROGRESS`, `DONE` | Valores permitidos aceites | Foram exercitados `TODO` por default, `IN_PROGRESS` numa atualização por Developer e `DONE` numa atualização por PM; não foi feito POST independente para cada valor. | Parcial |
| TC-06 | Aceitar prioridades permitidas | Integração | Tarefa acessível ao PM | `LOW`, `MEDIUM`, `HIGH` | Valores permitidos aceites | Foram exercitados `MEDIUM` por default, `HIGH` numa tarefa e `LOW` numa atualização; não foi feito POST independente para cada valor. | Parcial |
| TC-07 | Aplicar defaults ao omitir estado e prioridade | Integração | PM com permissão de gestão | POST sem `status` nem `priority` | `201`; `TODO` e `MEDIUM` | API devolveu `201`, `TODO` e `MEDIUM`. | Passou |
| TC-08 | Criar tarefa pela API e confirmar resposta | Integração | PM autenticado e projeto criado | POST com título e descrição válidos | `201`, IDs e cabeçalho `Location` | Criação devolveu `201`; IDs, campos e `Location` foram verificados. | Passou |
| TC-09 | Listar tarefas acessíveis | Integração | Utilizador com acesso e tarefa existente | GET da lista do projeto | `200`; lista contém apenas tarefas do projeto | GET devolveu `200`; o teste de persistência verificou a tarefa esperada na lista. | Passou |
| TC-10 | Consultar tarefa acessível | Integração | Utilizador com acesso e tarefa existente | GET do detalhe da tarefa | `200`; dados correspondem à tarefa | GET devolveu `200` e os dados corresponderam à representação criada. | Passou |
| TC-11 | Rejeitar título vazio na criação | Integração | PM com permissão de gestão | `title: ""` | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-12 | Rejeitar título só com espaços na criação | Integração | PM com permissão de gestão | `title: "   "` | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-13 | Rejeitar título abaixo do mínimo | Integração | PM com permissão de gestão | Título com 2 caracteres | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-14 | Rejeitar título acima do máximo | Integração | PM com permissão de gestão | Título com 151 caracteres | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-15 | Rejeitar descrição acima do máximo | Integração | PM com permissão de gestão | Descrição com 2001 caracteres | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-16 | Rejeitar estado não permitido na criação | Integração | PM com permissão de gestão | `status: "BLOCKED"` | `400`; tarefa não criada | API devolveu `400`; o teste verificou que não foi criada tarefa. | Passou |
| TC-17 | Rejeitar prioridade não permitida na criação | Integração | PM com permissão de gestão | `priority: "URGENT"` | `400`; tarefa não criada | Não foi testada prioridade inválida no POST. Foi testada prioridade inválida no PATCH (TC-20). | Por validar |
| TC-18 | Preservar tarefa após atualização inválida do título | Integração | PM autenticado; tarefa existente | PATCH com título vazio, só espaços, 2 ou 151 caracteres | `400`; título persistido inalterado | Não foi executado PATCH com título inválido. | Por validar |
| TC-19 | Preservar tarefa após atualização inválida do estado | Integração | PM autenticado; tarefa existente | PATCH com `status: "BLOCKED"` | `400`; estado persistido inalterado | Não foi executado PATCH com estado inválido. | Por validar |
| TC-20 | Preservar tarefa após atualização inválida da prioridade | Integração | PM autenticado; tarefa com prioridade conhecida | PATCH com `priority: "URGENT"` | `400`; prioridade persistida inalterada | API devolveu `400`; após recarregar a tarefa, a prioridade continuou `MEDIUM`. | Passou |
| TC-21 | Preservar tarefa após atualização inválida da descrição | Integração | PM autenticado; tarefa com descrição conhecida | PATCH com descrição de 2001 caracteres | `400`; descrição persistida inalterada | Não foi executado PATCH com descrição acima do limite. | Por validar |
| TC-22 | Impedir consulta direta por utilizador sem acesso | Integração | Developer autenticado, não associado ao projeto | GET da tarefa de outro projeto | `404`; conteúdo não revelado | GET da lista e detalhe devolveu `404`; no teste autenticado por sessão, o título privado não apareceu na resposta. | Passou |
| TC-23 | Impedir alteração por utilizador sem acesso | Integração | Developer autenticado, não associado ao projeto; tarefa existente | PATCH do estado | Pedido recusado e estado inalterado | PATCH devolveu `404`. Esse teste não verificou separadamente o valor persistido após a recusa. | Parcial |
| TC-24 | Enviar descrição explicitamente nula | Integração | PM com permissão de gestão | POST com `description: null` | Comportamento compatível com o contrato; semântica face à omissão a confirmar | Resposta devolveu `description: ""`; não foi comparada com um POST que omitisse o campo. | Parcial |
| TC-25 | Enviar descrição vazia ou só com espaços | Integração | PM com permissão de gestão | POST com `description: ""` e, separadamente, espaços | Comportamento a definir antes de fixar a asserção | Estes inputs não foram testados. | Por validar |
| TC-26 | Verificar espaços externos no título | Integração | PM com permissão de gestão | Criar tarefa com espaços externos no título | Título normalizado e limites respeitados | `"  Initial task  "` foi devolvido como `"Initial task"`; não foi testado um limite exato após a remoção dos espaços. | Parcial |
| TC-27 | Criar projeto e tarefa pela interface | E2E | Base E2E preparada; PM de demonstração | Iniciar sessão, criar projeto e tarefa `TODO` | Projeto/tarefa criados; fluxo visível; limpeza no teardown | 1 teste passou; projeto e tarefa devolveram `201`, tarefa apareceu como `TODO` e projeto foi eliminado com `204`. | Passou |

## 3. Testes Automatizados

| Ficheiro | Comando executado | Resultado real |
|---|---|---|
| `backend/apps/tasks/tests.py` | `.venv/bin/python backend/manage.py test apps.tasks` | 29 testes passaram; system check sem problemas. |
| Apps backend `accounts`, `projects`, `tasks`, `comments` | `.venv/bin/python backend/manage.py check && .venv/bin/python backend/manage.py test apps.accounts apps.projects apps.tasks apps.comments` | `check` sem problemas; 61 testes passaram. |
| `frontend/test/sessionExpired.test.js` | `cd frontend && npm test` | 3 testes passaram, 0 falharam. |
| Build frontend | `cd frontend && npm run build` | Build Vite concluído com sucesso. |
| `frontend/e2e/task-flow.spec.js` | `cd frontend && PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" npm run test:e2e` | 1 teste passou usando o Chrome instalado no sistema. |

Preparação E2E: a configuração Compose foi validada; a base isolada não tinha migrations pendentes e o seed não criou registos. O teste não usou a base de desenvolvimento.

## 4. Limitações e Problemas Conhecidos

- Não foram executados testes manuais. Em particular, a verificação de IDOR com duas sessões de demonstração continua por validar; os resultados de autorização acima são de testes automatizados e revisão estática. Ver também [quality-security-review.md](./quality-security-review.md).
- O teste E2E cobre o fluxo positivo de um Project Manager, não a matriz completa de papéis nem cenários negativos da interface.
- O primeiro arranque E2E não iniciou o teste porque faltava o browser gerido pelo Playwright. A execução foi repetida com o Chrome já instalado e passou.
- TC-03, TC-04, TC-17 a TC-19, TC-21 e TC-25 não foram executados. TC-05, TC-06, TC-23, TC-24 e TC-26 têm cobertura parcial, conforme indicado na tabela.
- O pedido não incluiu uma lista separada dos cenários do Exercício 1 nem os outputs originais dos Exercícios 2–4. A matriz usa os cenários TC-01 a TC-26 já existentes no repositório e regista apenas resultados observados nas execuções disponíveis.

## 5. Decisões Tomadas

- Não há registo de cenários sugeridos pela IA que tenham sido explicitamente alterados ou rejeitados por decisão humana; não se atribuem decisões não documentadas.
- Mantém-se TC-07 porque a US-04 e o OpenAPI definem defaults `TODO` e `MEDIUM`, e o teste da API confirmou esse comportamento. `constraints.md` também descreve o estado como obrigatório; a divergência documental não foi resolvida por este plano.
- Para o caso executado de acesso a uma tarefa de outro projeto, o resultado observado foi `404`. O teste de escrita sem acesso também recebeu `404`; não se infere além dos inputs e operações efetivamente testados.
- As semânticas de descrição omitida, vazia ou composta por espaços e a validação de limites exatos após normalização do título continuam sem decisão/teste conclusivo.

## Referências

- [Requisitos do MVP](./requirements.md)
- [User Stories e critérios de aceitação](./user-stories.md)
- [Restrições, pressupostos e decisões pendentes](./constraints.md)
- [Contrato OpenAPI](../openapi.yaml)
