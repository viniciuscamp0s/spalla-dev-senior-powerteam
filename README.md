# spalla-dev-senior-powerteam

**As habilidades de desenvolvimento com IA que usamos todo dia, num lugar só, prontas para instalar no Claude Code ou
no Codex.**

Planejar, executar com subagentes e com outro modelo, testar, depurar, revisar, checar segurança, economizar cota,
orquestrar várias sessões e caprichar no frontend. Agrupadas por função, com **crédito a cada autor** (superpowers,
plugins oficiais, impeccable, rtk e as demais), as nossas em versão universal e, principalmente, **os erros que já
cometemos construindo sistemas com IA, cada um virado em regra**.

O que você leva:

- **Um fluxo de ponta a ponta** (pedido → plano curto → execução → revisão → verificação → segurança → publicação), com
  a habilidade certa em cada etapa: [`docs/01-fluxo-de-ponta-a-ponta.md`](docs/01-fluxo-de-ponta-a-ponta.md).
- **Um guia de quando usar cada habilidade** (e quando não usar), por função:
  [`docs/02-guia-das-habilidades.md`](docs/02-guia-das-habilidades.md).
- **`/route`**: o Claude planeja e revisa como adversário, o Codex escreve o código. Quem escreve não aprova, e o
  código gasta a outra assinatura.
- **Checagem de segurança com 17 riscos + infra**, cada um com onde procurar, como provar e como corrigir, mais um
  varredor sem IA que roda em segundos.
- **Economia de cota medida**, não palpite: onde vão os tokens novos numa semana real e o que corta cada pedaço.
- **Uma trava de trabalho pesado** para várias sessões no mesmo computador não derrubarem umas às outras.
- **O padrão de engenharia** com as 10 regras de observabilidade de produção (request ID, log JSON, health detalhado,
  rollback automático...).
- **Mais de 45 erros reais viraram regra** em [`docs/06-erros-que-ja-cometemos.md`](docs/06-erros-que-ja-cometemos.md):
  publicação, testes, sessões e cota, execução paralela, segredos, git e delegação.

## Instalar

Cole no Claude Code ou no Codex o prompt de [`INSTALAR.md`](INSTALAR.md). A IA instala os plugins de terceiros pelos
comandos oficiais deles, copia as nossas skills e testa.

## Por onde começar

| Você quer | Leia |
|---|---|
| O caminho de um pedido até produção | [`docs/01-fluxo-de-ponta-a-ponta.md`](docs/01-fluxo-de-ponta-a-ponta.md) |
| Saber qual habilidade usar agora | [`docs/02-guia-das-habilidades.md`](docs/02-guia-das-habilidades.md) |
| Parar de bater no limite da assinatura | [`docs/03-economia-de-cota.md`](docs/03-economia-de-cota.md) |
| Rodar várias sessões sem caos | [`docs/04-orquestrar-sessoes.md`](docs/04-orquestrar-sessoes.md) |
| Padrão de engenharia e observabilidade | [`docs/05-padrao-de-engenharia.md`](docs/05-padrao-de-engenharia.md) |
| **Os erros e as travas (leia antes de publicar)** | [`docs/06-erros-que-ja-cometemos.md`](docs/06-erros-que-ja-cometemos.md) |
| As nossas skills | [`skills/README.md`](skills/README.md) |
| Quem fez cada habilidade de terceiros | [`CREDITOS.md`](CREDITOS.md) |

## Por função

| Função | Habilidades |
|---|---|
| Planejar | `superpowers:brainstorming`, `grill-me`, `superpowers:writing-plans`, `feature-dev` |
| Executar | [`route`](skills/route/SKILL.md), [`execucao-enxuta`](skills/execucao-enxuta/SKILL.md), `superpowers:subagent-driven-development`, `dispatching-parallel-agents`, `executing-plans`, `using-git-worktrees` |
| Testar | `superpowers:test-driven-development`, `verification-before-completion` |
| Depurar | `superpowers:systematic-debugging` |
| Revisar | `code-review`, `code-simplifier`, `superpowers:requesting-code-review`, `untangle-codebase` (diagnóstico) |
| Segurança | [`checagem-de-seguranca`](skills/checagem-de-seguranca/SKILL.md), `/security-review`, `claude-security` |
| Economia de cota | [spalla-senior-agente-economia-token](https://github.com/viniciuscamp0s/spalla-senior-agente-economia-token), `rtk` |
| Orquestrar sessões | [webster-maestro-de-agentes](https://github.com/viniciuscamp0s/webster-maestro-de-agentes), [`trava.sh`](ferramentas/trava.sh), [`checkpoint-de-raciocinio`](skills/checkpoint-de-raciocinio/SKILL.md), `claude-md-management`, `skill-creator`, `find-skills` |
| Frontend | `frontend-design`, `impeccable`, `ui-ux-pro-max`, `vercel-react-best-practices`, `web-design-guidelines`, `gsap-*`, `threejs-*` |

## O que não está aqui

Nenhum dado de cliente, nenhum nome de empresa, nenhum caminho de computador, nenhum segredo. As skills de terceiros
não são redistribuídas: a instalação baixa cada uma do repositório original, com a licença dela.

## Desenvolvimento

```bash
npm test                         # testes (node --test): estrutura das skills, links e a trava
node ferramentas/varredura.mjs   # varredura de privacidade antes de publicar um fork
```

## Licença e créditos

MIT. Feito por Vinicius Campos ([@viniciuscamp0s_](https://www.instagram.com/viniciuscamp0s_/) no Instagram), a
partir dos sistemas que construímos com IA. Habilidades e ferramentas de terceiros: ver [`CREDITOS.md`](CREDITOS.md).
