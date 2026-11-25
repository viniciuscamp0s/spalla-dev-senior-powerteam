# Instalar

Abra o Claude Code ou o Codex **na pasta do seu projeto** e cole o prompt abaixo. A IA instala sozinha e no fim
mostra o que ficou instalado.

```text
Instale as habilidades de desenvolvimento do repositório https://github.com/viniciuscamp0s/spalla-dev-senior-powerteam neste
projeto, seguindo o INSTALAR.md dele à risca:
1. Clone o repositório numa pasta spalla-dev-senior-powerteam/ dentro deste projeto (ou atualize com git pull se já existir) e
   ponha spalla-dev-senior-powerteam/ no .gitignore deste projeto.
2. Confira as ferramentas: node 20+, git, bash (no Windows, o Git Bash) e python 3. Para cada uma que faltar, me diga
   o comando de instalação do meu sistema e instale com o meu ok. Codex CLI e GitHub CLI são opcionais: pergunte.
3. Instale as nossas skills: copie cada pasta de spalla-dev-senior-powerteam/skills/ (menos o README.md) para .claude/skills/
   deste projeto. Se você for o Codex ou outro agente sem pasta de skills, crie ou complete o AGENTS.md apontando
   spalla-dev-senior-powerteam/docs/ como base e spalla-dev-senior-powerteam/skills/*/SKILL.md como procedimentos.
4. Se você for o Claude Code, me mostre os comandos de plugin abaixo para eu colar (são comandos de barra, só eu
   consigo rodar) e espere eu confirmar:
     /plugin marketplace add obra/superpowers-marketplace
     /plugin install superpowers@superpowers-marketplace
     /plugin marketplace add anthropics/claude-plugins-official
     /plugin install feature-dev@claude-plugins-official
     /plugin install code-review@claude-plugins-official
     /plugin install code-simplifier@claude-plugins-official
     /plugin install claude-security@claude-plugins-official
     /plugin install frontend-design@claude-plugins-official
     /plugin install skill-creator@claude-plugins-official
     /plugin install claude-md-management@claude-plugins-official
     /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
     /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
5. Instale as outras skills de terceiros a partir dos repositórios originais listados em spalla-dev-senior-powerteam/CREDITOS.md
   (impeccable com "npx impeccable install"; a untangle-codebase copiando só a pasta skills/untangle-codebase de
   caldoai/skills; as da Vercel, a grill-me, as gsap-* e as threejs-* com
   "npx skills add <dono>/<repo>" ou clonando numa pasta temporária e copiando só as pastas de skill para
   .claude/skills/), mantendo o LICENSE de cada uma. Não copie nada que a licença não permita. Pergunte antes de
   instalar gsap e threejs: só fazem sentido se eu mexo com animação ou 3D na web.
6. Economia de cota: instale o rtk pelo README de https://github.com/rtk-ai/rtk (rode "rtk init -g" no fim) e me
   ofereça a claude-economia-de-cota (https://github.com/viniciuscamp0s/spalla-senior-agente-economia-token). Não instale o
   plugin ponytail: o que só ele tinha já vem na nossa skill execucao-enxuta (veredito em
   spalla-dev-senior-powerteam/docs/03-economia-de-cota.md).
7. Rode o teste: cd spalla-dev-senior-powerteam && npm test.
8. Me mostre em até 8 linhas o que ficou instalado e qual habilidade usar em cada etapa (planejar, executar, testar,
   depurar, revisar, segurança, publicar), conforme spalla-dev-senior-powerteam/docs/02-guia-das-habilidades.md.
Regras: nada pago sem me dizer o custo antes; segredo (token, senha) eu colo direto no .env, nunca no chat; código de
terceiro só do repositório oficial listado no CREDITOS.md, e anote num spalla-dev-senior-powerteam/INSTALADO.md (fora do git) o
commit ou a versão de cada um que você instalou, para eu saber o que roda aqui.
```

## O que a instalação faz, passo a passo

| Passo | O que acontece | Quanto custa |
|---|---|---|
| Ferramentas | Node, git, bash, python | 0 (tudo aberto) |
| Skills nossas | `route`, `execucao-enxuta`, `checagem-de-seguranca`, `checkpoint-de-raciocinio` | 0 |
| Plugins de terceiros | superpowers e os plugins oficiais, pelos comandos `/plugin` de cada autor | 0 |
| Skills de terceiros | baixadas dos repositórios originais (lista e licenças em [`CREDITOS.md`](CREDITOS.md)) | 0 |
| Economia de cota | rtk e, se quiser, claude-economia-de-cota | 0 |
| Teste | `npm test` | alguns segundos |

## Instalação manual (sem IA)

```bash
git clone https://github.com/viniciuscamp0s/spalla-dev-senior-powerteam.git
cd spalla-dev-senior-powerteam
npm test
mkdir -p ../.claude/skills && cp -r skills/*/ ../.claude/skills/
```

Depois, no Claude Code, cole os comandos `/plugin` do passo 4 do prompt acima. Quer em todos os seus projetos? Copie
as skills para `~/.claude/skills/` em vez de `.claude/skills/`.

## Usar a trava de trabalho pesado

```bash
bash spalla-dev-senior-powerteam/ferramentas/trava.sh pesada npm run build
```

Ponha no seu `CLAUDE.md` (ou `AGENTS.md`): "build, suíte inteira de testes, npm ci e deploy rodam sempre por
`bash spalla-dev-senior-powerteam/ferramentas/trava.sh pesada <comando>`".

## Atualizar

`cd spalla-dev-senior-powerteam && git pull`, depois copie de novo as pastas de `skills/`. Os plugins se atualizam pelo próprio
`/plugin` do Claude Code. O que mudou em cada versão: [`CHANGELOG.md`](CHANGELOG.md).
