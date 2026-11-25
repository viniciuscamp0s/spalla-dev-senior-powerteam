# Economia de cota

A assinatura do Claude é orçamento de construção. O que gasta a cota não é o tamanho da conversa: é o que entra de
**novo** (entrada, saída e escrita de cache). Reler o cache quase não pesa.

## Onde os tokens novos vão (medido numa semana real de uso intenso)

| O que aconteceu | Parte dos tokens novos |
|---|---|
| Contexto reescrito inteiro depois de pausa de mais de 1 hora (o cache venceu) | **22,7%** |
| Subagentes (57% deles no modelo mais caro, a maioria só lendo e buscando) | 11,4% |
| Abrir uma sessão nova (mediana) | cerca de 83 mil tokens por sessão |
| Sessões com mais de 150 respostas | a maior parte do resto |

## As quatro ferramentas e o que cada uma corta

| Ferramenta | Corta | Sobreposição com as outras |
|---|---|---|
| [claude-economia-de-cota](https://github.com/viniciuscamp0s/claude-economia-de-cota) (nossa) | reescrita de cache depois de pausa, custo de abertura de sessão, sessão longa, subagente no modelo caro | — |
| [rtk](https://github.com/rtk-ai/rtk) | a **saída dos comandos** (git, testes, ls, busca) antes de entrar no contexto | nenhuma |
| [ponytail](https://github.com/DietrichGebert/ponytail) | o **texto que o modelo escreve** (prompt de "escreva o mínimo" injetado por ganchos) | praticamente nenhuma |
| `/compact` com foco, ou resumo de passagem | o contexto de uma sessão que ficou grande demais | complementa a primeira |

## Veredito sobre o ponytail

Analisamos o ponytail contra a nossa ferramenta antes de decidir. Ele é um prompt de "escreva o mínimo" ligado por
ganchos (`SessionStart`, `SubagentStart`, `UserPromptSubmit`): corta tokens de **saída**. A nossa corta a reescrita de
cache, a abertura de sessão e o modelo de subagente, que no nosso uso pesavam muito mais. Não competem.

**Mantemos a nossa como base e deixamos o ponytail como complemento opcional, em teste:**

1. Instale sem o painel e sem webhook, com o mapa desligado (`PONYTAIL_MAP=0`).
2. Rode uma semana e compare os tokens novos com a semana anterior (o diagnóstico da claude-economia-de-cota faz a
   conta).
3. Economizou menos de 5%? Desligue.
4. **Risco a vigiar:** o modo "mínimo" pode reduzir escopo (entregar menos do que foi pedido) e brigar com a régua de
   qualidade. Se uma entrega voltar incompleta, ele sai.

## Disciplina que vale mais que qualquer ferramenta

1. **Uma sessão, uma entrega.** Fechou a entrega, ou passou de ~150 respostas: resumo de passagem e sessão nova.
2. **Espera longa nunca acorda sessão com o cache vencido.** Sessão que espera (build, testes, outra sessão) acorda em
   menos de 1 hora ou encerra com passagem. Espera de horas grava o ponto de parada e encerra.
3. **Tudo que entra no contexto custa.** Ler por trecho (busca, faixa de linhas), nunca arquivo grande inteiro, nem
   relido sem ter mudado. Saída de comando filtrada (`head`, `grep`, `--quiet`, contagem em vez de lista). Log de
   teste e de build só nas linhas de erro.
4. **Abrir sessão tem preço fixo** (o CLAUDE.md inteiro entra de novo). Não abra sessão para o que cabe em poucas
   respostas na que já está aberta. CLAUDE.md curto: regra com ponteiro, o porquê em arquivo lido sob demanda.
5. **Subagente leva o modelo na chamada:** barato para ler, intermediário para conferir, forte só para julgar.
6. **Resposta enxuta também é economia:** editar por trecho, sem repetir arquivo inteiro, sem relatório que ninguém
   pediu.
7. **Código quem escreve pode ser outra assinatura:** a skill [`route`](../skills/route/SKILL.md) põe o Codex para
   escrever e o Claude para planejar e revisar.

## Resumo de passagem (handoff)

Quando a sessão fecha no meio de um trabalho, a próxima começa por um arquivo curto e operacional, nunca por uma ata:

```markdown
# Passagem: <tarefa>
- Objetivo e critério de pronto: ...
- Feito (com a prova): ...
- Falta, em ordem: ...
- Decisões tomadas e por quê: ...
- Onde está cada coisa (arquivos, branch, comandos): ...
- Armadilhas já encontradas: ...
```
