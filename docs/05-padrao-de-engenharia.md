# Padrão de engenharia

O que vale para todo sistema que construímos com IA. Base: o
[vibe-coding-toolkit](https://github.com/soumatheusgomes/vibe-coding-toolkit) de Matheus Gomes (MIT), adotado com as
divergências da seção 3 e com as 10 regras de observabilidade da seção 4, que acrescentamos.

## 1. Como usar o toolkit

| Momento | O que rodar no toolkit | Condição |
|---|---|---|
| Sistema novo | `docs/prompts/11-next-project-bootstrap.md` | Com as regras de observabilidade desde o primeiro commit |
| Melhorar sistema existente | `docs/prompts/12-existing-project-setup.md` | Um sistema por sessão, plano aprovado antes de executar |
| Arquivo grande demais | `docs/prompts/09-file-size-refactor.md` | Só no arquivo que a tarefa já está mexendo |
| Revisão de código | `docs/prompts/03-multi-agent-code-review.md` ou o plugin `code-review` | Ciclos proporcionais ao risco |
| Pedido vago | `docs/prompts/04-brainstorm-to-plan.md` ou `superpowers:brainstorming` | Antes de qualquer código |

**Use uma cópia fixada num commit, nunca o link do `main`:** o repositório muda todo dia e vários comandos usam
`@latest`. Ferramenta aberta entra com versão fixada.

## 2. Acordos (valem em todo sistema)

1. **Menor mudança completa.** Reutilizar o que existe; nada de abstração, opção ou dependência que ninguém pediu.
2. **Arquivo presente ≠ configurado ≠ testado.** "Pronto" diz qual dos três foi provado, com o comando que provou.
3. **Correção de bug vem com reprodução e teste de regressão** quando viável.
4. **Validar fronteira em runtime** (Zod ou equivalente) em formulário, rota, webhook e resposta de API externa. Tipo
   TypeScript não é validação.
5. **Teto de 350 linhas por arquivo de código novo.** Legado não se refatora em massa: arquivo que a tarefa já mexe e
   passa do teto ganha divisão por responsabilidade quando for barato.
6. **Segredo nunca em log**, nem em mensagem montada à mão (a redação de campos do logger não limpa texto livre).
7. **Delegação com contrato:** cada subagente recebe objetivo, arquivos permitidos, aceite e checks; um escritor por
   arquivo; revisor só lê; o coordenador confere o diff antes de aceitar.
8. **Retomada confere o real** (git, arquivos, processos), nunca confia só no resumo da sessão anterior.
9. **Documento responsável muda junto** com comportamento, comando, schema ou fronteira, no mesmo commit.
10. **Todo domínio nasce com ícone de app:** apple-touch-icon de 180 px, manifest com nome e ícones (192 e 512),
    favicon e theme-color, para o atalho "Adicionar à Tela de Início" sair com a marca. O ícone é a logo oficial,
    colada por código; sistema com vários hosts tem teste que falha se um host ficar sem ícone.
11. **Senha mínima de 8 caracteres**, e nunca mais que isso como exigência: regra visível, botão de mostrar senha e
    entrada direta depois de criar. Exigência alta vira barreira e gente travada no primeiro acesso.
12. **Sistema com chance de abrir ao público tem o botão "ver como o cliente":** o administrador entra na visão de um
    cliente e enxerga exatamente o que ele enxerga, sem a senha dele, com a troca registrada e uma faixa visível.
13. **Toda tela nova nasce aberta a todo usuário da conta; a exceção é o dinheiro.** Restringir uma tela pede motivo
    escrito. Quando o dado sensível aparece dentro de uma tela de trabalho, restringe-se o bloco, não a tela inteira,
    e as ações e as regras do banco daquela tela abrem junto.

## 3. Onde divergimos do toolkit (e por quê)

| O toolkit diz | Nós fazemos | Motivo |
|---|---|---|
| Drizzle + PostgreSQL | Mantemos o banco e o ORM que o sistema já usa; sistema novo decide no plano | O próprio toolkit proíbe migrar ORM como efeito do setup |
| ESLint com regras locais | Biome no pre-commit | Mesma função, mais rápido; o toolkit cobre Biome |
| Sem hook de pre-commit/pre-push | Trava de segredo + typecheck + lint no pre-commit, testes no pre-push | Segredo vazado é prioridade máxima; hook é trava técnica, não preferência |
| 3 a 8 ciclos de revisão após cada implementação | Proporcional ao risco, com o custo estimado: 1 em mudança comum, 3+ em dinheiro, auth, banco e dado pessoal | Orçamento de tokens |
| Plugins de "escreva menos" injetados em toda sessão | Opcionais, em teste de uma semana (ver [`03-economia-de-cota.md`](03-economia-de-cota.md)) | Medir antes de adotar |
| Nove documentos de projeto | Preservar o documento canônico que o projeto já tem; sistema novo usa os nove | Nunca criar fonte concorrente |
| `AGENTS.md` compartilhado + `CLAUDE.md` ponte | Adotado em sistema novo; nos existentes, quando o Codex passar a executar ali com frequência | O Codex lê `AGENTS.md`, não `CLAUDE.md` |

## 4. Observabilidade de produção: as 10 regras preventivas

Valem com ferramentas abertas: nenhuma plataforma paga de monitoramento é pré-requisito.

| # | Regra | Como cumprir | Mínimo aceitável |
|---|---|---|---|
| 1 | Toda requisição tem **request ID único** | Gerar no middleware (`crypto.randomUUID()`), devolver no header `x-request-id` e levar em todo log da requisição | Header + campo `requestId` no log de erro |
| 2 | Todo erro tem **stack trace e contexto** | Logger grava `err.stack`, escopo, `requestId` e IDs do objeto (nunca dado pessoal ou segredo) | Stack guardado, não só impresso |
| 3 | Todo log é **JSON estruturado** | Pino (com redação de segredo) ou o logger atual emitindo JSON | Uma linha JSON por evento, com `level`, `scope`, `requestId`, `msg` |
| 4 | Todo serviço tem **health check detalhado** | `/api/health` (vivo) + `/api/health/deep` (banco, filas, integrações, cada um com status e tempo) + `HEALTHCHECK` no Dockerfile | Deep devolve 503 quando uma dependência crítica cai |
| 5 | Todo acesso ao banco tem **log de query com tempo** | Opção de log do query builder ou wrapper no cliente; registrar só acima de um limiar (ex.: 300 ms) | Query lenta vira log com duração e nome da operação, nunca o valor dos parâmetros |
| 6 | Todo cache tem **contagem de hit/miss** | Contador no módulo de cache, exposto no deep health | Só onde já existe cache |
| 7 | Todo serviço tem **métricas de tempo, memória e CPU** | Duração por rota no log; `process.memoryUsage()` e `process.cpuUsage()` no deep health; `docker stats` no servidor | Memória e duração visíveis sem entrar no servidor |
| 8 | Todo fluxo crítico tem **teste de regressão** | Testes no pre-push; dinheiro, autenticação e mensagem a cliente sempre cobertos | Bug corrigido ganha o teste que teria pego ele |
| 9 | Todo sistema tem **alerta configurável de anomalia** | Canal de alertas com limite e silêncio em configuração | Nunca alerta por erro isolado |
| 10 | Todo deploy tem **monitoramento com rollback automático** | O script de deploy confere o deep health depois de subir e, se falhar após N tentativas, volta sozinho para a imagem anterior e avisa | Rollback sem humano; o manual fica como plano B |

**Proporção:** sistema de uma tela ou script interno cumpre 2, 3, 8 e 9; o resto entra quando houver usuário externo,
banco ou deploy próprio.

**Ordem de ataque num sistema que já existe (maior ganho por menor custo):** 10 (o script já guarda a imagem anterior,
falta executar a volta) → 1, 2 e 3 juntas no logger central (um arquivo muda, todo ponto que já chama o logger herda)
→ 9 → 5 e 7 no deep health → 6 só quando um cache for tocado.

## 5. Antes de dizer "pronto" em qualquer sistema

- Typecheck limpo, lint limpo, testes do que foi tocado verdes, build ok.
- Mudança visível conferida na tela, na largura de um celular quando for interface.
- Nenhuma das 10 regras piorou (log novo é JSON, erro novo leva stack, rota nova passa pelo request ID).
- Deploy só pelo script do sistema, conferido no deep health depois de subir.
- Fase da [`checagem-de-seguranca`](../skills/checagem-de-seguranca/SKILL.md).
