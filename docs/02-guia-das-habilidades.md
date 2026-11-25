# Guia das habilidades: quando usar cada uma

Agrupadas por função. A coluna "quando" é o gatilho; a coluna "não use para" evita a habilidade errada no lugar
certo. Autor e licença de cada uma: [`CREDITOS.md`](../CREDITOS.md).

## Planejar

| Habilidade | Quando | Não use para |
|---|---|---|
| `superpowers:brainstorming` | Pedido novo ou vago, antes de qualquer código | Correção pequena com escopo óbvio |
| `grill-me` | Você já tem um plano e quer que ele seja atacado pergunta a pergunta | Gerar o plano do zero |
| `superpowers:writing-plans` | Trabalho de várias etapas com spec definida | Tarefa de um arquivo |
| `feature-dev` | Funcionalidade que pede explorar o código, desenhar arquitetura e revisar no fim | Script isolado |

## Executar com subagentes e com outro modelo

| Habilidade | Quando | Não use para |
|---|---|---|
| [`route`](../skills/route/SKILL.md) (nossa) | Tarefa delimitada; o Claude planeja e revisa, o Codex escreve | Arquitetura, pedido vago |
| `superpowers:subagent-driven-development` | Plano com tarefas independentes, um subagente por tarefa | Tarefas que mexem no mesmo arquivo |
| `superpowers:dispatching-parallel-agents` | 2 ou mais investigações sem estado compartilhado | Trabalho sequencial |
| `superpowers:executing-plans` | Executar você mesmo, na sessão, um plano escrito | — |
| `superpowers:using-git-worktrees` | Trabalho paralelo isolado do branch principal | Mudança de um minuto |

Subagente leva o modelo na chamada: o mais barato para busca e leitura em volume, o intermediário para extração e
conferência, o mais forte só para julgamento.

## Testar e verificar

| Habilidade | Quando |
|---|---|
| `superpowers:test-driven-development` | Toda funcionalidade com regra de negócio e toda correção de bug |
| `superpowers:verification-before-completion` | Antes de dizer "pronto", "corrigido" ou "passou" |

## Depurar

| Habilidade | Quando |
|---|---|
| `superpowers:systematic-debugging` | Qualquer bug, teste falhando ou comportamento estranho, **antes** de propor correção |

## Revisar

| Habilidade | Quando |
|---|---|
| `code-review` | Revisão do diff atual ou de um pull request |
| `superpowers:requesting-code-review` / `receiving-code-review` | Pedir revisão com contexto; receber revisão sem concordar por educação |
| `code-simplifier` | Depois de aprovado, para tirar o excesso sem mudar comportamento |
| `superpowers:finishing-a-development-branch` | Decidir como integrar o branch (merge, PR, limpeza) |

## Segurança

| Habilidade | Quando |
|---|---|
| [`checagem-de-seguranca`](../skills/checagem-de-seguranca/SKILL.md) (nossa) | Fim de toda implementação que cria ou muda superfície |
| `/security-review` (Claude Code) | Revisão de segurança das mudanças do branch |
| `claude-security` (plugin) | Varredura completa de um repositório, com triagem e correção |

## Economia de cota

| Habilidade | Quando |
|---|---|
| [claude-economia-de-cota](https://github.com/viniciuscamp0s/claude-economia-de-cota) (nossa) | Bater no limite antes do fim da semana; medir onde vão os tokens novos e ligar as correções |
| `rtk` | Sempre: corta a saída de `git`, testes, `ls`, busca antes de entrar no contexto |
| `ponytail` | Opcional, em teste de uma semana (veredito em [`03-economia-de-cota.md`](03-economia-de-cota.md)) |

## Orquestrar sessões

| Habilidade | Quando |
|---|---|
| [maestro-generico](https://github.com/viniciuscamp0s/maestro-generico) (nosso) | Você quer falar com um agente só que divide, escolhe modelo, abre e acompanha as sessões |
| [`trava.sh`](../ferramentas/trava.sh) (nossa) | Várias sessões no mesmo computador rodando build e testes |
| [`checkpoint-de-raciocinio`](../skills/checkpoint-de-raciocinio/SKILL.md) (nossa) | Um "sempre" ou "nunca" que tem de virar regra permanente |
| `claude-md-management` | Manter o CLAUDE.md curto e atual |
| `skill-creator`, `superpowers:writing-skills`, `find-skills` | Criar, medir e achar skills |

## Frontend

| Habilidade | Quando |
|---|---|
| `frontend-design` | Direção visual de uma tela nova, para não sair com cara de template |
| `impeccable` | Crítica, auditoria e polimento (hierarquia, tipografia, cor, movimento, acessibilidade) |
| `ui-ux-pro-max` | Escolher estilo, paleta, par de fontes e regras de UX por tipo de produto |
| `vercel-react-best-practices` | Escrever ou revisar React/Next.js com desempenho |
| `web-design-guidelines` | Auditar a interface pelas Web Interface Guidelines |
| `gsap-*` | Animação de interface e scroll |
| `threejs-*` | Cena 3D na web |
