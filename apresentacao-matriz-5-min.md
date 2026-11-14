# Matriz — guião para apresentação final

**Duração máxima: 5 minutos, incluindo a demonstração.** Não são necessários diapositivos: abre a aplicação e usa este documento como guião.

| Tempo | Momento |
|---|---|
| 0:00–0:30 | Enquadramento |
| 0:30–2:40 | Demonstração: painel e gestão de uma tarefa |
| 2:40–3:20 | Tecnologias e arquitetura |
| 3:20–4:00 | Metodologia e utilização de IA |
| 4:00–4:45 | Desafio, solução e aprendizagem |
| 4:45–5:00 | Limites e conclusão |

## Antes de começar

- Abre [Matriz no Render](https://matriz-project-manager-web.onrender.com/) e confirma que a página responde. O plano gratuito pode demorar a despertar.
- Inicia sessão antecipadamente com a conta de demonstração de Project Manager. Usa a password que configuraste, sem a mostrar no ecrã nem a colocar no guião.
- Confirma que o projeto **Planeamento de demonstração** e a tarefa **Preparar plano** estão visíveis. Se entretanto tiverem sido alterados, escolhe outro projeto e tarefa de demonstração.
- Mantém como alternativa a aplicação local em <http://localhost:5174/>, mas apenas se estiver preparada com conta e dados de demonstração próprios.
- Abre o [repositório GitHub](https://github.com/simcampos/matriz---project-manager) e garante que o formador tem acesso. A entrega é feita pelo URL do repositório, não por este guião.
- Fecha separadores com credenciais, configurações e dados pessoais. Ensaia com cronómetro.

---

## 0:00–0:30 — Enquadramento

**Diz:**

> O Matriz é uma aplicação web para ajudar uma equipa a organizar projetos e tarefas e acompanhar o seu progresso. O objetivo deste MVP é juntar, num único lugar, o trabalho, os responsáveis e os estados das tarefas, com acesso adequado a cada perfil.

> Vou mostrar brevemente como um gestor acompanha um projeto e atualiza uma tarefa.

## 0:30–2:40 — Demonstração

### Fluxo 1 — Acompanhar projetos e progresso

**Mostra no ecrã:**

1. Com sessão iniciada como Project Manager, abre o **Painel**.
2. Mostra os projetos acessíveis e as contagens de tarefas por estado.
3. Abre **Projetos** e seleciona **Planeamento de demonstração**.

**Diz:**

> No painel vejo os projetos a que tenho acesso e uma visão rápida do progresso. Ao abrir um projeto, encontro as respetivas tarefas. Isto permite perceber o que está por fazer, em progresso ou concluído.

### Fluxo 2 — Gerir uma tarefa

**Mostra no ecrã:**

1. Na lista de tarefas, abre **Preparar plano** ou outra tarefa de demonstração.
2. Mostra o estado, a prioridade e os responsáveis. Se o tempo permitir, mostra os comentários.
3. Edita o estado da tarefa e guarda. Mostra o resultado na lista ou no detalhe.
4. Se houver tempo, aplica um filtro por estado ou prioridade.

**Diz:**

> Como Project Manager, posso gerir as tarefas do meu projeto, incluindo estado, prioridade e responsáveis. O Developer, por sua vez, pode atualizar o estado das tarefas que lhe estão atribuídas e a que tem acesso. O Admin pode consultar projetos e tarefas, mas não os alterar.

**Se a demonstração atrasar:** não cries dados novos nem tentes resolver configurações em direto. Mostra apenas o painel e uma tarefa existente e passa à arquitetura.

## 2:40–3:20 — Tecnologias e arquitetura

**Diz:**

> A interface foi construída com React e Vite. No backend usamos Python, Django e Django REST Framework, que disponibilizam a API. Os dados ficam em PostgreSQL.

> A autenticação usa sessões geridas pelo Django e proteção CSRF. O backend está organizado em módulos, como contas, projetos, tarefas e comentários. Para a demonstração, a aplicação está disponibilizada no Render.

**Esquema opcional para apontar:**

`Browser → React → API Django/DRF → PostgreSQL`

## 3:20–4:00 — Metodologia e IA

**Diz:**

> Organizei o trabalho a partir dos requisitos e histórias de utilizador, passando pela implementação, testes e documentação. Usei ferramentas de IA como apoio à análise, à escrita e revisão de código e ao diagnóstico de problemas, sem assumir que as respostas estavam sempre corretas.

> As propostas foram verificadas contra os requisitos, o código, os resultados dos testes e os logs. No GitHub Actions, os testes correm antes da publicação e do pedido de deploy na branch principal.

## 4:00–4:45 — Desafio, solução e aprendizagem

**Diz:**

> Ao preparar os dados no Render, o runner teve problemas de ligação e os logs mostraram migrations pendentes. Aplicámo-las na base de dados existente e carregámos os dados de demonstração pela rede interna.

> A aprendizagem foi que ter ligação à base de dados não significa que o esquema esteja pronto. Atualmente, as migrations futuras não correm automaticamente no deploy. Uma opção gratuita seria executá-las no arranque da API, mas ainda não foi implementada e exige cuidado com a compatibilidade das versões.

## 4:45–5:00 — Limites e conclusão

**Diz:**

> O resultado é um MVP para demonstração. No plano gratuito, a base de dados expira ao fim de 30 dias e não tem backups automáticos. A gestão de contas, a recuperação de acesso e outras questões de segurança e operação continuam por definir.

> Em resumo, o Matriz permite organizar trabalho, acompanhar o progresso e aplicar permissões por perfil. Obrigado.

---

## Checklist de entrega e perguntas

- [ ] Aplicação preparada e demonstração ensaiada dentro dos cinco minutos.
- [ ] Repositório acessível ao formador: <https://github.com/simcampos/matriz---project-manager>.
- [ ] README com funcionalidades, tecnologias, pré-requisitos e instruções de execução.
- [ ] Código e configuração necessários, incluindo exemplo de ambiente sem segredos.
- [ ] Confirmar que ficheiros de ambiente reais, passwords, tokens e dados pessoais desnecessários não são incluídos na entrega.
- [ ] Submeter o URL do GitHub no espaço indicado pelo formador.

**Se perguntarem sobre testes:** há testes automatizados para backend e frontend e um fluxo E2E documentado. Nem todos os cenários e combinações de perfis foram validados manualmente.

**Se perguntarem sobre produção:** o Render atual é um ambiente de protótipo; faltam decisões e validações de segurança, gestão de contas, recuperação e operação antes de o tratar como produção.

**Se perguntarem sobre migrations e deploy:**

- Atualmente, o GitHub Actions testa e pede o deploy, mas não aplica migrations na base de dados Render. Se o novo código precisar de tabelas ou colunas ainda não criadas, pode falhar.
- Uma opção gratuita, ainda não implementada, é executar `migrate` no arranque da API antes do Gunicorn. Se a migration falhar, a nova API não arranca; o comando também é executado em reinícios, mas o Django não reaplica migrations já registadas.
- O frontend é lançado separadamente e a pipeline atual não confirma que os deploys ficaram ativos. O código anterior pode continuar a funcionar durante o deploy, pelo que alterações de esquema incompatíveis exigem planeamento; um rollback da aplicação não reverte a base de dados.
- O Render disponibiliza um comando de pré-deploy em planos pagos. A base de dados gratuita expira ao fim de 30 dias e não disponibiliza backups automáticos; é inadequada para dados de produção. Ver [deploys](https://render.com/docs/deploys) e [limitações gratuitas](https://render.com/docs/free).
