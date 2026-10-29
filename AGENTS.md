# Instruções para agentes — Matriz

## Antes de começar

- Antes de executar qualquer tarefa, consulta `docs/requirements.md`, `docs/user-stories.md` e `docs/constraints.md`, bem como outros documentos relevantes em `docs/`.
- Se a documentação estiver em conflito, incompleta ou não cobrir um requisito necessário, identifica a dúvida e pede clarificação antes de tomar uma decisão que altere o âmbito ou o comportamento do produto.

## Requisitos e âmbito

- Trata os factos comunicados pelo cliente como distintos dos pressupostos e propostas. Não apresentes pressupostos como decisões aprovadas.
- Respeita os requisitos, critérios de aceitação, restrições e limites do MVP documentados.
- Não inventes funcionalidades, regras de negócio, permissões, integrações, tecnologias ou decisões de arquitetura. Propõe opções e solicita aprovação quando uma decisão não estiver documentada.
- Mantém as alterações focadas na tarefa. Atualiza a documentação relacionada quando os requisitos aprovados mudarem.

## Planeamento e aprovação

- Antes de alterações significativas, apresenta um plano breve com o âmbito e os ficheiros ou áreas afetados.
- Aguarda aprovação antes de iniciar alterações significativas que mudem o âmbito, contratos, comportamento central ou dados do produto.
- Pede aprovação explícita antes de ações destrutivas ou sensíveis, incluindo eliminar ou substituir dados/ficheiros, alterar histórico, publicar informação, fazer deployment ou modificar credenciais e configurações de acesso.
- Se não houver aprovação, não executes a ação; explica o impacto e sugere uma alternativa segura quando possível.

## Segurança e confidencialidade

- Não exponhas, copies para documentação ou incluas em respostas credenciais, tokens, chaves, dados pessoais desnecessários ou outra informação confidencial.
- Não introduzas segredos no repositório. Se encontrares informação potencialmente sensível, evita reproduzi-la e alerta o utilizador de forma segura.
- Aplica as regras de acesso e privacidade documentadas; não alargues permissões por conveniência.

## Comunicação e validação

- Comunica os pressupostos usados e assinala os que ainda precisam de confirmação.
- No final, resume as alterações realizadas e indica as verificações executadas e os respetivos resultados. Em tarefas somente de leitura, indica que não alteraste ficheiros e resume os achados; se não foi possível validar algo, explica o motivo.
- Não afirmes que testes, builds, publicação ou outras ações foram concluídos sem os ter executado e verificado.
