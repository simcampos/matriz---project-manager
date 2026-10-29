# Análise inicial de requisitos — Matriz

## Contexto

Descrição recebida do cliente:

> "Precisamos de uma aplicação onde as nossas equipas possam organizar projetos, gerir tarefas e acompanhar o progresso do trabalho."

Esta análise separa o que foi explicitamente informado do que ainda precisa de validação. Nenhum pressuposto abaixo deve ser tratado como requisito confirmado.

## Factos conhecidos

- O produto pretendido é uma aplicação.
- As equipas devem poder organizar projetos.
- As equipas devem poder gerir tarefas.
- As equipas devem poder acompanhar o progresso do trabalho.
- Não foram especificados utilizadores, fluxos, regras de negócio, integrações, escala, requisitos de segurança ou prioridades.

## Pressupostos a validar

- Cada pessoa terá uma conta individual e poderá pertencer a uma ou mais equipas.
- Existirão papéis diferentes, como administrador, gestor de projeto e membro da equipa.
- Um projeto conterá tarefas, e as tarefas terão responsáveis, estados, prioridades e prazos.
- As equipas poderão colaborar nas tarefas, por exemplo através de comentários ou anexos.
- O progresso será calculado a partir do estado das tarefas ou apresentado em painéis e relatórios.
- A aplicação poderá enviar notificações ou integrar-se com ferramentas já usadas pelo cliente.
- Os projetos e tarefas poderão conter informação confidencial que exija controlo de acesso.
- A aplicação terá de suportar um número específico de utilizadores, equipas e projetos, embora essa escala ainda seja desconhecida.

## Perguntas de clarificação

1. **Utilizadores e equipas:** Quem utilizará a aplicação (por exemplo, membros da equipa, gestores ou administradores)? Como se organizam as pessoas em equipas e quem pode criar ou gerir cada equipa?
2. **Acesso e permissões:** Que ações devem estar disponíveis para cada tipo de utilizador? O acesso a projetos e tarefas será limitado por equipa, projeto ou outro critério?
3. **Organização dos projetos:** Que informação define um projeto e como deve ser organizado o trabalho dentro dele? Um projeto pode envolver várias equipas?
4. **Gestão de tarefas:** Que informação uma tarefa deve conter e que operações são necessárias no dia a dia (criar, atribuir, editar, comentar, anexar ficheiros, entre outras)?
5. **Fluxo de trabalho:** Que estados e transições uma tarefa pode ter? As equipas precisam de configurar os seus próprios fluxos, prioridades ou regras?
6. **Acompanhamento do progresso:** O que significa “progresso” para o cliente? Que vistas, métricas ou relatórios ajudariam a acompanhar projetos e tarefas?
7. **Colaboração e notificações:** Como devem as pessoas comunicar sobre o trabalho e que acontecimentos devem gerar notificações? Por que canais?
8. **Integrações:** A aplicação precisa de trocar informação com ferramentas ou serviços existentes, como sistemas de identidade, comunicação, calendário ou gestão de código? Quais e em que sentido?
9. **Escala e utilização:** Quantos utilizadores, equipas, projetos e tarefas são esperados inicialmente e num horizonte futuro? Há requisitos de disponibilidade ou de utilização simultânea?
10. **Segurança e dados:** Que tipos de informação serão guardados e que requisitos existem para autenticação, proteção de dados, auditoria, retenção ou eliminação?

## Próximo passo

Recolher as respostas às perguntas acima e, com base nelas, definir o âmbito inicial do produto, os fluxos prioritários e os requisitos funcionais e não funcionais a detalhar.
