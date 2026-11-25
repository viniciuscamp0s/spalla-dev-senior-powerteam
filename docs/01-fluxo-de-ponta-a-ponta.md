# O fluxo de ponta a ponta

Do pedido ao que está no ar, nesta ordem. Cada etapa diz a habilidade que usamos e o que conta como pronto. Pule
etapas só quando a mudança é pequena de verdade (um arquivo, sem entrada nova de fora): aí vão o passo 3 e o 5.

```text
pedido ──> 1. enquadrar ──> 2. plano curto ──> 3. execução ──> 4. revisão ──> 5. verificação
                                                                                     │
                            8. registro <── 7. publicação <── 6. segurança <─────────┘
```

## 1. Enquadrar o pedido

Separe três coisas: **o que é entrega**, **o que é decisão de quem pediu** (escopo, prioridade, dinheiro, texto que
vai para cliente) e **o que já está feito ou rodando** (outra sessão, um branch, um processo). Pergunte só o que é
decisão; acesso, permissão e "como rodar" são trabalho seu.

- Pedido vago: `superpowers:brainstorming` (uma pergunta por vez até o desenho fechar) ou `grill-me` (entrevista
  implacável sobre um plano que já existe).
- Retomando trabalho: confira o real (git, arquivos, processos) antes de confiar no resumo da sessão anterior.

**Pronto quando:** você consegue escrever o critério de pronto numa frase.

## 2. Plano curto

Decisões, arquivos e testes. Nada de plano de dez páginas: plano longo é cota gasta antes do código.

- `superpowers:writing-plans` para trabalho de várias etapas.
- `feature-dev` quando a funcionalidade pede exploração do código e escolha de arquitetura.
- Mudança estrutural (renomear, mover, trocar a base): investigue tudo, mostre o plano, espere o sim, só então execute.

**Pronto quando:** cada etapa tem arquivo, teste e critério; o que está fora de escopo está escrito.

## 3. Execução

Escolha o executor pelo tipo de trabalho:

| Situação | Como executar |
|---|---|
| Tarefa delimitada e você tem Codex | [`route`](../skills/route/SKILL.md): o Claude escreve o `PLAN.md`, o Codex escreve o código, o Claude revisa |
| Várias tarefas independentes | `superpowers:subagent-driven-development` ou `dispatching-parallel-agents`, cada subagente com contrato (objetivo, arquivos permitidos, aceite) |
| Execução na própria sessão | `superpowers:executing-plans` |
| Código com regra de negócio | `superpowers:test-driven-development`: o teste que falha vem antes |
| Bug | `superpowers:systematic-debugging`: reproduzir, achar a causa, só então corrigir, com teste de regressão |
| Interface | `frontend-design` para a direção, `impeccable` e `ui-ux-pro-max` para o acabamento, `web-design-guidelines` para a auditoria |

Regras que valem em toda execução: menor mudança completa; um escritor por arquivo; trabalho pesado (build, suíte de
testes, deploy) pela [trava](../ferramentas/trava.sh), um por vez no computador.

## 4. Revisão

Quem escreveu não aprova. Revisão do diff inteiro, como adversário: o plano foi seguido? o escopo cresceu? há caso de
borda, código morto, abstração prematura?

- `code-review` (plugin oficial) ou `superpowers:requesting-code-review`.
- `code-simplifier` depois de aprovado, para tirar o excesso.
- Quantidade de ciclos proporcional ao risco: 1 em mudança comum; 3 ou mais em dinheiro, autenticação, banco e dado
  pessoal.

## 5. Verificação

`superpowers:verification-before-completion`: rodar o comando que prova e ler a saída antes de dizer "pronto".
**Arquivo presente não é configurado, e configurado não é testado**: o relato diz qual dos três foi provado e com qual
comando. Interface se confere na tela de verdade, na largura de um celular.

## 6. Segurança

[`checagem-de-seguranca`](../skills/checagem-de-seguranca/SKILL.md) no fim de toda implementação que cria ou muda uma
superfície (rota, formulário, webhook, IA, porta). Varredor sem IA primeiro; depois as perguntas dos 17 riscos que a
mudança toca. Bloqueador achado = não publica. Para varredura ampla, o plugin `claude-security`.

## 7. Publicação

- Publicar é parte da entrega: **editado e não publicado não é entregue**. O que roda em produção é a versão
  publicada, não o arquivo.
- Deploy só pelo script do sistema, conferido no health check depois de subir, com volta automática para a versão
  anterior se falhar.
- Antes de publicar, confira o que está no ar: outra frente pode ter publicado depois de você.

## 8. Registro

O que mudou de comportamento muda o documento responsável no mesmo commit. Decisão importante vai para um diário
(append-only, com data e o porquê). Commit só dos seus arquivos, nunca `git add -A` numa pasta compartilhada.
Fechou a entrega: feche a sessão e a worktree que abriu.
