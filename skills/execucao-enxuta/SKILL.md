---
name: execucao-enxuta
description: Regras de código mínimo para a FASE DE EXECUÇÃO (escrever o código de um plano já aprovado). Use ao implementar um PLAN.md, no prompt do executor da skill route, ou quando pedirem "menor mudança", "sem abstração", "código enxuto". Nunca no planejamento nem na revisão (lá ela cortaria escopo ou critério). Não reduz o que foi pedido.
license: MIT
---

# Execução enxuta

A regra-mãe é a **menor mudança completa** (acordo 1 do padrão de engenharia, em `docs/05-padrao-de-engenharia.md`):
reutilizar o que existe, nada de abstração, opção ou dependência que ninguém pediu. Esta skill não repete o acordo:
traz só o que ele não diz, para a hora de escrever o código. Vale **só na execução**: no planejamento e na revisão,
"faça o mínimo" vira corte de escopo e de critério.

## Escopo primeiro, depois o mínimo

Antes de escrever, liste todo lugar que a mudança precisa alcançar: quem chama, testes, fixtures, configuração,
exports, e o que ela pode quebrar ou expor para quem usa. **Isso é escopo e se entrega inteiro.** Preguiça é na
solução, nunca na mudança: tudo o que o pedido e o plano mandam fazer, se faz. Esta skill nunca encolhe um pedido.

## A escada (pegue o primeiro degrau que resolve por inteiro)

1. Já existe neste código (helper, componente, serviço, padrão)? Use do jeito que o código em volta usa.
2. A biblioteca padrão ou a plataforma resolve? Use, a menos que o projeto tenha o seu próprio (componente da casa
   ganha do nativo).
3. Uma dependência já instalada resolve? Use. Nunca acrescente dependência por poucas linhas.
4. Cabe numa linha que se entende de primeira? Uma linha.
5. Senão: o mínimo de código que funciona.

## O que muda na escrita

- **Apagar ganha de acrescentar.** Mantenha a estrutura que o código já tem (camadas, interfaces, convenções) e os
  valores na forma que a plataforma já entrega, sem conversão nem embrulho.
- **O menor diff vence**, depois de saber tudo o que ele precisa tocar. Uma linha que precisa ser decifrada não é curta.
- **Comentário só para o porquê** que o código não mostra, em uma linha.
- **Correção de bug:** antes de editar, procure todos os que chamam a função e corrija a causa uma vez, no código
  compartilhado.
- **Código movido ou juntado mantém** o tratamento de erro e a validação que tinha.
- **Entre duas opções do mesmo tamanho**, a que acerta os casos de borda.
- **Lógica nova não trivial leva a sua prova:** um teste pequeno ou uma autoverificação (ramo, laço, parser, dinheiro,
  segurança, script novo). Mudança trivial dispensa.
- **Atalho com limite conhecido leva o comentário** `atalho: <o limite>, <quando trocar>`. A dívida fica achável:
  `rg -n "atalho:"` lista tudo o que foi deixado para depois.

## Nunca se corta

Validação na fronteira de confiança, tratamento de erro que evita perda de dado, segurança, acessibilidade, a
calibração que o hardware real pede, e qualquer coisa que o pedido ou o plano mandaram.

## Fecho

Termine a resposta com uma ou duas linhas: o que ficou de fora ou não foi conferido, e o risco que quem pediu precisa
saber.

---
Adaptado das regras do [ponytail](https://github.com/DietrichGebert/ponytail) (Copyright (c) 2026 DietrichGebert,
licença MIT), só a parte que não repete o nosso padrão de engenharia, sem a regra de entregar "a menor versão" de um
pedido vago (aqui o escopo é do plano) e sem os ganchos, o painel e o webhook do plugin.
