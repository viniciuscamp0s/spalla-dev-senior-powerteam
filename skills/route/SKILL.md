---
name: route
version: 2.0.0
description: |
  Loop de dois modelos para tarefas de implementação: o Claude planeja e revisa, o Codex CLI executa o código.
  Só ativa com o comando explícito /route "<tarefa>", nunca em conversa normal. Ideal para trabalho de
  implementação delimitado ("adiciona validação X", "cria endpoint Y", "escreve testes para Z"). Não é para
  discussão de arquitetura nem para tarefa vaga sem escopo claro.
license: MIT
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# /route: o Claude planeja e revisa, o Codex executa

Você é o diretor técnico. O Codex é o executor. A regra de ouro: **você nunca escreve o código de produção
diretamente**. Você escreve o plano, delega a implementação ao Codex e revisa o resultado como adversário até
aprovar.

Por que dois modelos: quem escreve o código não é quem o aprova. O revisor não tem apego ao que leu, e a
assinatura que mais gasta (a do executor) não é a mesma que guarda o julgamento.

## 0. Pré-requisitos (conferir os dois antes de qualquer coisa)

### 0.1 Localizar o binário do Codex

```bash
CODEX="$(command -v codex || true)"
```

Se vier vazio, procure a instalação do app desktop. No Windows o app guarda o binário numa pasta com hash que muda a
cada atualização automática: **escolha a pasta mais recente que tem o executável completo** (no Windows, `codex.exe`
**e** `codex-code-mode-host.exe`). Durante uma atualização o app deixa pastas incompletas, e o `exec` numa delas
falha sem escrever nada.

```bash
# Windows (Git Bash), exemplo:
for d in $(ls -t -d "$LOCALAPPDATA"/OpenAI/Codex/bin/*/ 2>/dev/null); do
  if [ -f "$d/codex.exe" ] && [ -f "$d/codex-code-mode-host.exe" ]; then CODEX="$d/codex.exe"; break; fi
done
```

Se continuar vazio, avise que é preciso instalar o Codex CLI (ou abrir o app uma vez) e pare.

O modelo padrão vem do `~/.codex/config.toml`. Não passe `-m` a menos que o usuário peça outro modelo.

### 0.2 A pasta é um repositório git?

O passo 3 revisa por `git diff`, e o git é a **única rede de segurança** contra o executor estragar código existente.

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

- **Repositório com a árvore limpa:** segue.
- **Repositório com mudanças não commitadas:** avise que o diff do executor vai se misturar ao trabalho do usuário e
  pergunte se ele quer commitar ou guardar antes. Nunca commite nem guarde por conta própria.
- **Não é repositório:** pergunte antes de rodar: `git init` (recomendado: dá diff e volta), seguir sem rede de
  segurança (a revisão lê os arquivos inteiros) ou abortar. Pasta só com arquivos novos pode seguir sem git; pasta com
  código do usuário, insista no `git init`.

## 1. Reescrever a tarefa num PLAN.md

Leia o pedido (`/route "<tarefa>"`). Explore o código relevante o suficiente para escrever um plano concreto, nunca
genérico. Grave em `PLAN.md` na raiz da pasta de trabalho:

- Objetivo em 1 ou 2 frases
- Arquivos que serão tocados (caminhos exatos, já conferidos)
- O que implementar, passo a passo, sem ambiguidade
- Critério de pronto (o que tem de ser verdade no fim)
- Fora de escopo (o que o executor NÃO toca)

Tarefa vaga demais para escopar sem chutar: pare e pergunte antes de escrever o plano.

Se já existe um `PLAN.md` que não é seu (outra sessão na mesma pasta), **não sobrescreva**: use `PLAN-<frente>.md` e
diga o nome no prompt do passo 2.

```bash
PLAN_FILE="PLAN.md"   # ou PLAN-<frente>.md
```

## 2. Delegar ao Codex

Modo não interativo, escrita liberada só no workspace, sem esperar aprovação:

```bash
cd "<raiz do repo>" && "$CODEX" exec -C "$(pwd)" -s workspace-write -c model_reasoning_effort=high \
  "Implemente o $PLAN_FILE exatamente como está escrito. Não toque em nada fora do escopo descrito nele. Escreva o código seguindo as regras de .claude/skills/execucao-enxuta/SKILL.md, se existir (código mínimo, sem cortar nada do plano)." \
  < /dev/null
```

Por que cada pedaço (aprendido na prática):

- **`-C <pasta>` é obrigatório**, senão o Codex recusa com `Not inside a trusted directory`. No Windows com Git Bash,
  use `"$(pwd -W)"`: o `.exe` entende o caminho no formato do Windows.
- **`cd` no mesmo comando.** A pasta atual da ferramenta de terminal pode voltar ao início entre chamadas.
- **`< /dev/null`.** O Codex tenta ler a entrada padrão; fechar evita qualquer espera.
- **Sem `-a never`.** Versões recentes removeram a flag; o `exec` já roda sem aprovação.

Deixe terminar e guarde a saída: ela traz o id da sessão, útil para retomar no passo 4.

### 2.1 O Codex bateu no limite de uso da conta

Só a mensagem literal de limite de uso (`You've hit your usage limit`, com o horário de volta) conta. Qualquer outro
erro (binário não achado, sandbox, rede, pasta não confiável) é problema de ambiente: volte ao passo 0.

Confirmado o limite, troque de executor **só nesta rodada**:

- Você escreve o código seguindo o plano com o MESMO rigor que cobraria do Codex: passo a passo, sem inventar, sem
  aumentar o escopo.
- Depois, faz o passo 3 sobre o próprio diff como se fosse de outra pessoa.
- No resumo e na mensagem de commit, registre que esta rodada foi escrita pelo Claude por causa do limite.
- Na próxima tarefa volta a ser o Codex quem escreve.

### 2.2 O modelo está lotado

`Selected model is at capacity` **não é limite de uso** e não autoriza o 2.1. Tente uma vez de novo; se repetir, rode
a mesma chamada com `-m <outro modelo do Codex>`. Registre no resumo qual modelo saiu. Confira sempre a mensagem de
hoje, nunca a de ontem: anotação antiga dizendo "sem cota" já mascarou um erro de outra natureza.

## 3. Revisar como adversário

- **Em repositório git:** `git status` + `git diff` (e `git diff --stat` se for grande).
- **Fora de repositório:** liste o que foi criado ou alterado e leia cada arquivo inteiro. Sem diff, a leitura tem de
  ser mais cuidadosa, não menos.

Procure:

- O plano foi seguido à risca, ou o executor inventou ou aumentou o escopo?
- Bugs e casos de borda não tratados
- Segurança: a fase da skill `checagem-de-seguranca` sobre o diff. Bloqueador de segurança reprova a rodada
- Complexidade desnecessária, código morto, abstração prematura
- Falta de teste onde o plano pedia teste

Não corrija você mesmo. Aqui o seu papel é só achar o problema.

## 4. Iterar ou aprovar

- **Achou problema real:** escreva a correção específica (o que está errado e o que deve virar) e retome a sessão
  anterior para manter o contexto:
  ```bash
  cd "<raiz do repo>" && "$CODEX" exec -C "$(pwd)" -s workspace-write resume --last \
    -c model_reasoning_effort=high "<correção específica>" < /dev/null
  ```
  A ordem importa: `-C` e `-s` são do `exec` e vêm **antes** de `resume`; `--last` e `-c` são do `resume` e vêm
  depois. Trocar dá `unexpected argument '-s'`. Volte ao passo 3.
- **Aprovou:** siga para o passo 5.
- **Trava:** depois de 3 rodadas sem aprovação, pare e pergunte se o usuário quer continuar, assumir à mão ou abortar.
  Nunca gire o laço sozinho gastando cota.

## 5. Fechar

Apague o `$PLAN_FILE` (era artefato de trabalho), a menos que o usuário peça para manter, e confira com
`git ls-files` que ele não entrou em nenhum commit (já aconteceu de um plano ser varrido para dentro do repositório
pelo commit de outra sessão). Resuma: o que foi pedido, quantas rodadas levou, o que mudou e o diff final.
**Não faça commit nem push**: isso é decisão do usuário, mesmo com o resultado aprovado.
