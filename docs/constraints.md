# Restrições e pressupostos — Matriz

## Factos explicitamente comunicados pelo cliente

- O cliente precisa de uma aplicação para as suas equipas.
- As equipas devem poder organizar projetos, gerir tarefas e acompanhar o progresso do trabalho.

## Pressupostos fornecidos para o MVP

- O acesso será feito através de um browser web.
- Os perfis considerados são Admin, Project Manager e Developer.
- A escala de referência é uma equipa pequena/média, até cerca de 50 utilizadores; não é um limite funcional confirmado.
- A autenticação prevista é por email e palavra-passe.
- Não haverá integrações externas no MVP.
- O MVP deve cobrir autenticação, gestão de projetos e tarefas, atribuição de tarefas e visualização de progresso.
- Não foram escolhidas tecnologias, frameworks ou arquiteturas.

## Pressupostos assumidos

Estes pontos orientam a documentação, mas ainda carecem de confirmação:

- O MVP começa com uma equipa; suportar várias equipas fica fora do âmbito inicial.
- Cada utilizador tem um papel principal entre Admin, Project Manager e Developer; acumulação de papéis não está definida.
- Admin pode consultar utilizadores existentes e atribuir papéis; o alcance do seu acesso aos projetos está por definir.
- Project Manager gere os projetos a que tem acesso e associa membros aos projetos.
- Developer consulta projetos aos quais está associado e atualiza o estado das tarefas que lhe foram atribuídas.
- Uma tarefa pertence a um único projeto. A proposta atual permite uma tarefa sem responsável e prevê no máximo um responsável.
- Título e estado são obrigatórios para tarefas; descrição é opcional. Para projetos, título é obrigatório e descrição opcional. Estes campos são propostas ainda por confirmar.
- Os estados propostos são “Por fazer”, “Em progresso” e “Concluída”.
- O progresso inicial será apresentado como contagem de tarefas por estado e lista de tarefas em aberto, definida provisoriamente como estado diferente de “Concluída”.
- “Até cerca de 50 utilizadores” é uma referência de dimensionamento fornecida para o MVP, não um limite máximo funcional acordado.
- Campos, permissões e fluxos definidos nos documentos são propostas para validação, não decisões finais do cliente.

## Segurança e privacidade

### Contexto conhecido

- A autenticação prevista é por email e palavra-passe.
- Existem papéis distintos e o acesso a projetos deverá ser limitado aos utilizadores autorizados, de acordo com o âmbito funcional proposto.
- Os dados deverão incluir, pelo menos, contas de utilizador, informação de projetos e informação de tarefas.
- Não foram fornecidos requisitos específicos de privacidade, proteção de dados, auditoria ou retenção.

### Regras propostas para validação

- Não apresentar nem permitir alterar projetos, tarefas ou progresso a utilizadores sem autorização para o projeto.
- Recusar alterações que o papel do utilizador não permite.
- Confirmar quais dados pessoais são necessários, quem pode consultá-los e por quanto tempo são conservados.
- Confirmar requisitos aplicáveis de auditoria, eliminação de contas/dados e resposta a incidentes.

As regras acima não especificam mecanismos de implementação e não devem ser interpretadas como requisitos técnicos fechados.

### Propostas mínimas de segurança por aprovar

- Uma tentativa sem autorização não deve revelar nem permitir alterar os dados do projeto, das tarefas ou do resumo.
- Mensagens de autenticação não devem indicar se o email está registado.
- Credenciais e sessões devem ser protegidas; a política concreta, recuperação de conta, expiração de sessão e prevenção de tentativas abusivas precisam de definição antes da produção.

### Privacidade por definir

Antes da produção, identificar os dados pessoais tratados, a finalidade de cada dado, quem pode aceder, a retenção e eliminação e quaisquer requisitos legais aplicáveis. Nenhum prazo ou obrigação legal específico foi fornecido.

## Decisões técnicas ainda pendentes

- Linguagens, frameworks, bibliotecas e ferramentas de desenvolvimento.
- Arquitetura da aplicação e desenho dos componentes.
- Sistema de armazenamento e modelo de dados.
- Serviço e mecanismo de autenticação, gestão de sessões e recuperação de acesso.
- Ambientes de execução, alojamento, deployment e estratégia de operação.
- Estratégia de testes, observabilidade, backups e recuperação.
- Browsers e versões que serão suportados.

Nenhuma tecnologia ou arquitetura deve ser assumida a partir deste documento.

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

Ficam fora do âmbito inicial: notificações, comentários, anexos, automações, importação, relatórios históricos, gráficos de tendência, vistas adicionais, subtarefas, dependências, marcos, múltiplas equipas e permissões granulares. A inclusão futura exige validação e priorização.

## Questões abertas

- Confirmar as permissões de cada papel, o alcance do Admin e o modelo de associação a projetos.
- Confirmar os campos obrigatórios e se tarefas podem ficar sem responsável.
- Definir o ciclo de vida de contas, recuperação de acesso e proteção de sessões.
- Definir dados pessoais tratados, finalidade, retenção e eliminação.
- Definir critérios verificáveis de segurança e privacidade.
- Definir objetivos mensuráveis de desempenho, disponibilidade, acessibilidade e compatibilidade.
- Confirmar se a escala de referência e o limite de uma equipa são adequados.
- Definir como tratar projetos arquivados, utilizadores removidos, falhas de gravação e alterações concorrentes.
