# Créditos

Este repositório junta as habilidades de desenvolvimento que usamos todos os dias com o Claude Code e o Codex. Uma
parte é nossa (os documentos, as skills em [`skills/`](skills/) e as ferramentas). A maior parte são skills, plugins e
ferramentas abertas de terceiros: **elas não são redistribuídas aqui**. Apontamos para o repositório original, com
autor e licença conferidos no próprio repositório em 25/11/2026, e a instalação baixa de lá. Todo o mérito delas é de
quem as fez.

Se você é autor de uma delas e quer outra forma de crédito, abra uma issue.

## Skills e plugins de terceiros, por função

| Função | Skill ou plugin | Autor | Repositório original | Licença |
|---|---|---|---|---|
| Planejar, executar, testar, depurar, revisar (o método inteiro) | `superpowers`: `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `writing-skills` | Jesse Vincent (obra) | [obra/superpowers](https://github.com/obra/superpowers) | MIT |
| Construir uma funcionalidade com exploração, arquitetura e revisão | `feature-dev` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Revisar código | `code-review` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Simplificar código | `code-simplifier` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Segurança (varredura e triagem) | `claude-security` (plugin oficial) e o comando `/security-review` do Claude Code | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Frontend com direção visual | `frontend-design` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Criar e medir skills | `skill-creator` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Manter o CLAUDE.md enxuto e atual | `claude-md-management` (plugin oficial) | Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Apache-2.0 |
| Padrão de engenharia (prompts de projeto novo, setup de projeto existente, refatoração, revisão multiagente) | `vibe-coding-toolkit` | Matheus Gomes (soumatheusgomes) | [soumatheusgomes/vibe-coding-toolkit](https://github.com/soumatheusgomes/vibe-coding-toolkit) | MIT |
| Economia de cota: saída de comandos | `rtk` (Rust Token Killer) | rtk-ai | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Apache-2.0 |
| Economia de cota: texto do modelo (opcional, ver o veredito em [`docs/03-economia-de-cota.md`](docs/03-economia-de-cota.md)) | `ponytail` | Dietrich Gebert | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT |
| Frontend: crítica, auditoria e polimento de interface | `impeccable` | Paul Bakaus | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 |
| Frontend: estilos, paletas, fontes e regras de UX | `ui-ux-pro-max` | nextlevelbuilder | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT |
| Frontend: React e Next.js com desempenho | `vercel-react-best-practices` | Vercel | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT (declarada no frontmatter da skill) |
| Frontend: revisão pelas Web Interface Guidelines | `web-design-guidelines` | Vercel | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | conferir no repositório (sem arquivo LICENSE na raiz em 25/11/2026) |
| Animação na web | `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-frameworks` | GreenSock | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | MIT (a biblioteca GSAP tem licença própria, gratuita inclusive para uso comercial) |
| 3D na web | `threejs-fundamentals`, `-geometry`, `-materials`, `-lighting`, `-textures`, `-animation`, `-loaders`, `-shaders`, `-postprocessing`, `-interaction` | CloudAI-X | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) | MIT |
| Afiar um plano antes do código (entrevista implacável) | `grill-me` | Matt Pocock | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT |
| Achar e instalar skills | `find-skills` e a CLI `npx skills` | Vercel | [vercel-labs/skills](https://github.com/vercel-labs/skills) | MIT |

**Passagem de sessão (handoff).** Usamos uma skill de compactação de contexto (`compactador-de-contexto`) cuja origem
não conseguimos confirmar: por isso ela não entra aqui. O equivalente aberto é o próprio `/compact` do Claude Code com
uma instrução de foco, ou o resumo de passagem descrito em [`docs/03-economia-de-cota.md`](docs/03-economia-de-cota.md).

## Ferramentas abertas

| Ferramenta | Licença | Uso aqui |
|---|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | termos da Anthropic | o agente onde tudo roda |
| [Codex CLI](https://github.com/openai/codex) | Apache-2.0 | executor da skill `route` |
| [GitHub CLI](https://github.com/cli/cli) | MIT | publicar repositório, conferir alertas de segurança |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | MIT / Unlicense | busca dos riscos 13 a 17 |
| [Node.js](https://nodejs.org) | MIT | testes e ferramentas deste repositório |

## Base da checagem de segurança

Os riscos 01 a 12 da skill [`checagem-de-seguranca`](skills/checagem-de-seguranca/SKILL.md) partem do guia "Vibe coding
com segurança" (KipperDev, set/2026). O texto da skill, as perguntas por stack, os riscos 13 a 17 e o varredor são
nossos.

## O que é nosso (criado por nós)

| Peça | O que é |
|---|---|
| [`skills/route`](skills/route/SKILL.md) | o Claude planeja e revisa, o Codex executa |
| [`skills/checagem-de-seguranca`](skills/checagem-de-seguranca/SKILL.md) | 17 riscos + infra, com varredor sem IA |
| [`skills/checkpoint-de-raciocinio`](skills/checkpoint-de-raciocinio/SKILL.md) | transforma um "sempre/nunca" em regra permanente no lugar certo |
| [`ferramentas/trava.sh`](ferramentas/trava.sh) | um trabalho pesado por vez no PC, entre todas as sessões |
| [`docs/`](docs/) | o fluxo de ponta a ponta, o guia das habilidades, o padrão de engenharia, os erros que já cometemos |
| [claude-economia-de-cota](https://github.com/viniciuscamp0s/claude-economia-de-cota) | diagnóstico e correção de desperdício de cota (repositório próprio, MIT) |
| [maestro-generico](https://github.com/viniciuscamp0s/maestro-generico) | o Maestro: um agente só que divide, escolhe modelo, abre e acompanha as sessões (repositório próprio) |

Tudo o que é nosso: MIT, por Vinicius Campos ([@viniciuscamp0s_](https://www.instagram.com/viniciuscamp0s_/) no
Instagram). O padrão de engenharia ([`docs/05-padrao-de-engenharia.md`](docs/05-padrao-de-engenharia.md)) adota e
adapta acordos do vibe-coding-toolkit, com crédito ao autor.
