# Orquestrar sessões

Quando você passa a rodar várias sessões de IA ao mesmo tempo, o gargalo deixa de ser o modelo e vira a
organização: quem faz o quê, em qual modelo, quem está parado esperando você, e o computador aguentando.

## Um agente só para falar com você: o Maestro

O [webster-maestro-de-agentes](https://github.com/viniciuscamp0s/webster-maestro-de-agentes) (nosso, aberto) é o jeito de trabalhar em que
você fala com um agente só. Ele:

1. **Enquadra** o pedido: separa entrega, decisão sua e o que já está rodando em outra sessão.
2. **Divide em etapas**, cada uma com critério de pronto.
3. **Escolhe o modelo de cada etapa** pelo que ela exige (tabela abaixo).
4. **Abre ele mesmo as sessões** de execução, acompanha cada uma até o fim e traz para você só o que é decisão.
5. Tem um **vigia** sem IA que retoma sozinha a sessão que caiu (internet, memória, computador reiniciado).

## Modelo por tipo de trabalho

| Trabalho | Modelo | Por quê |
|---|---|---|
| Diagnóstico difícil, arquitetura, decisão com muitas variáveis | o mais forte | julgamento; uma sessão, um problema, nunca sessão longa de construção |
| Construção a partir de plano preciso, revisão de código | intermediário-alto | entrega bem com plano bom, por um custo muito menor por resposta |
| Componente isolado bem especificado, conferência mecânica, script simples | intermediário | mesmo resultado quando o plano fecha o escopo |
| Busca ampla e leitura em volume (subagente que devolve só a conclusão) | o mais barato | ler é barato |
| Código a partir de plano curto | Codex pela skill [`route`](../skills/route/SKILL.md) | gasta a outra assinatura; o Claude revisa |

Sinal para trocar no meio: o trabalho mudou de natureza (de diagnóstico para construção em volume, desce; de
construção para arquitetura travada, sobe), ou a sessão passou de ~150 respostas. **O modelo mais forte numa sessão
longa de construção é o erro mais caro.**

## Regras de convivência entre sessões

- **Uma pasta, uma sessão.** Duas sessões na mesma pasta pisam uma na outra (arquivo, `PLAN.md`, commit). Trabalho
  paralelo vai em worktree própria (`superpowers:using-git-worktrees`).
- **Um trabalho pesado por vez no computador.** Build, suíte inteira de testes, `npm ci` e deploy passam pela
  [`trava.sh`](../ferramentas/trava.sh); ler, escrever e planejar seguem em paralelo, sem esperar.
- **Etapa que não depende da outra nunca espera na fila.** Aprovação ou publicação de uma não segura a outra.
- **Pergunta é decisão.** Acesso, permissão, pasta e "como rodar" a sessão resolve sozinha; só sobe a você o que é
  escolha sua (escopo, dinheiro, texto que vai para fora, ação destrutiva em dado real).
- **Quem abre fecha.** Entrega fechada: a sessão e a worktree que ela abriu se fecham (o branch fica).
- **Confira as outras sessões antes de dar status.** Se a transcrição mais nova de outra sessão contradiz o estado que
  você tem, vale a transcrição.

## A trava, em uma linha

```bash
bash ferramentas/trava.sh pesada npm test
```

Espera a vez (até 8 min por padrão; nunca mais de 45, para a sessão não acordar com o cache vencido), roda o
comando, solta a trava e devolve o código de saída dele. Trava de processo morto se desfaz sozinha.
