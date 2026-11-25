---
name: checkpoint-de-raciocinio
description: Ensina um "modo de pensar" novo à sua estrutura de IA, de forma permanente. Use quando o usuário invocar /checkpoint-de-raciocinio ou disser "isso é um checkpoint", "aprenda esse modo de pensar", "quero que você repita esse raciocínio sozinho da próxima vez", ou quando ele corrigir um raciocínio com "sempre" ou "nunca". Não executa tarefa: captura o padrão por trás de um raciocínio que acabou de acontecer e grava na skill ou no documento de regras que vai usá-lo de novo.
license: MIT
---

# Checkpoint de raciocínio

Uma tarefa se faz uma vez. Um **modo de pensar**, depois de capturado, tem de se repetir sozinho toda vez que a
situação voltar, sem ninguém reexplicar. Esta skill é o mecanismo de captura.

Exemplos do que vira checkpoint: um jeito de cruzar dados que ninguém tinha pensado; uma pergunta que tem de vir
sempre antes de outra; um critério de decisão que só ficou claro depois do porquê; uma armadilha que já causou erro uma
vez e não pode se repetir.

**A meta-regra:** quando o usuário diz "sempre" ou "nunca", não é comentário sobre a tarefa, é regra permanente. Ela é
gravada na hora, no lugar certo. Fazer a pessoa repetir uma regra que já deu é falha de processo.

## Como agir quando invocado

1. **Ler o raciocínio** que o usuário acabou de descrever (na mensagem do comando ou na troca imediatamente anterior).
2. **Abstrair o padrão:** tirar o exemplo específico e escrever a regra geral por trás dele. Exemplo: de "dividir a
   frota de carros elétricos pelos pontos de recarga da cidade" para "cruzar duas métricas relacionadas revela a
   tensão entre oferta e demanda melhor que uma métrica isolada". Se a generalização não for óbvia, pergunte em vez de
   chutar.
3. **Achar a casa do padrão:** qual skill ou documento vai USAR esse modo de pensar de novo? Quase sempre uma skill que
   já existe; raramente justifica uma nova. **Toda regra tem um lugar só**: se ela já mora em algum arquivo, edite lá;
   nunca escreva uma segunda cópia.
4. **Gravar como instrução permanente e reaplicável**, não como registro de episódio. Formato: um bloco
   `### Checkpoint: <nome curto>` com a regra geral primeiro, o porquê depois e, se ajudar, o exemplo original como
   ilustração.
5. **Confirmar em 1 a 3 linhas:** o que foi capturado, em que arquivo e quando deve disparar daí em diante.

## Regras

- Cirúrgico: só acrescenta o checkpoint; nunca reescreve o resto do arquivo-alvo.
- Já existe um checkpoint do mesmo raciocínio em outro contexto? Funde, não duplica.
- Checkpoint específico demais (só serve para aquele caso) não vale gravar: pergunte o que generalizar.
- Regra aposentada morre em todos os lugares: ao trocar uma regra, procure e apague todas as cópias antigas.
- O objetivo é a estrutura pensar melhor sozinha, não documentar o que já foi feito.
