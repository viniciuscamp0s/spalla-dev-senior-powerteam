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
| [spalla-senior-agente-economia-token](https://github.com/viniciuscamp0s/spalla-senior-agente-economia-token) (nossa) | reescrita de cache depois de pausa, custo de abertura de sessão, sessão longa, subagente no modelo caro | — |
| [rtk](https://github.com/rtk-ai/rtk) | a **saída dos comandos** (git, testes, ls, busca) antes de entrar no contexto | nenhuma |
| [ponytail](https://github.com/DietrichGebert/ponytail) | o **código que o modelo escreve** (regras de "escreva o mínimo") | só com o nosso acordo 1; o resto virou a skill `execucao-enxuta` |
| `/compact` com foco, ou resumo de passagem | o contexto de uma sessão que ficou grande demais | complementa a primeira |

## Veredito sobre o ponytail

O ponytail é um prompt de "escreva o mínimo de código" ligado por ganchos (`SessionStart`, `SubagentStart`,
`UserPromptSubmit`). Fizemos o mapa de sobreposição antes de decidir:

| O que o ponytail faz | O que já tínhamos | Decisão |
|---|---|---|
| Menor mudança completa: reusar, nada de abstração, opção ou dependência não pedida | Acordo 1 do [padrão de engenharia](05-padrao-de-engenharia.md) | Igual: fica numa casa só, a nossa |
| "Nunca corte validação, erro, segurança" | Acordos 4 e 6 e a [checagem de segurança](../skills/checagem-de-seguranca/SKILL.md) | Igual: nossa |
| Escada de reuso (código da casa → biblioteca padrão → dependência instalada → uma linha) | — | **Só ele tem: entra** |
| Comentário `atalho: <limite>, <quando trocar>` e a lista de dívida | — | **Só ele tem: entra** |
| Autoverificação em lógica não trivial; fecho com o que ficou sem conferir | TDD do superpowers (parcial) | **Entra como complemento** |
| "Pedido vago ganha a menor versão" | Escopo é do plano aprovado | **Fica de fora**: corta escopo |
| Painel de custo por tarefa (ledger), webhook | [spalla-senior-agente-economia-token](https://github.com/viniciuscamp0s/spalla-senior-agente-economia-token) mede a cota | Fica de fora: duplicaria |
| Mapa do repositório injetado na abertura | — | Fica de fora: custa tokens em toda sessão |
| Corta a saída de comandos | [rtk](https://github.com/rtk-ai/rtk) | Não faz; sem sobreposição |
| Corta reescrita de cache, abertura e sessão longa | claude-economia-de-cota | Não faz; sem sobreposição |

**Forma escolhida:** em vez de instalar o plugin, o que só ele tem virou a skill
[`execucao-enxuta`](../skills/execucao-enxuta/SKILL.md) (MIT, com crédito), carregada **só na fase de execução**
(no prompt do executor da [`route`](../skills/route/SKILL.md)). Motivo: os ganchos do plugin injetam o texto em toda
abertura de sessão, em todo subagente e checam toda mensagem, inclusive no planejamento e na revisão, onde "faça o
mínimo" vira corte de escopo. Como skill, custa zero fora da execução.

**Medição:** uma semana comparando, nas sessões de execução, tokens de saída e linhas adicionadas por tarefa contra a
semana anterior. Economizou menos de 5%, ou alguma entrega voltou com escopo cortado: sai.

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
