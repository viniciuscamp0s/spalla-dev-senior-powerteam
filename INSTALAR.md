# Instalar

Abra o Claude Code ou o Codex **na pasta do seu projeto** e cole o prompt abaixo. A IA instala sozinha e no fim
mostra o que ficou instalado.

```text
Instale as habilidades de desenvolvimento do repositório https://github.com/viniciuscamp0s/habilidades-dev neste
projeto, seguindo o INSTALAR.md dele à risca:
1. Clone o repositório numa pasta habilidades-dev/ dentro deste projeto (ou atualize com git pull se já existir) e
   ponha habilidades-dev/ no .gitignore deste projeto.
2. Confira as ferramentas: node 20+, git, bash (no Windows, o Git Bash) e python 3. Para cada uma que faltar, me diga
   o comando de instalação do meu sistema e instale com o meu ok. Codex CLI e GitHub CLI são opcionais: pergunte.
3. Instale as nossas skills: copie cada pasta de habilidades-dev/skills/ (menos o README.md) para .claude/skills/
   deste projeto. Se você for o Codex ou outro agente sem pasta de skills, crie ou complete o AGENTS.md apontando
   habilidades-dev/docs/ como base e habilidades-dev/skills/*/SKILL.md como procedimentos.
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
5. Instale as outras skills de terceiros a partir dos repositórios originais listados em habilidades-dev/CREDITOS.md
   (impeccable com "npx impeccable install"; as da Vercel, a grill-me, as gsap-* e as threejs-* com
   "npx skills add <dono>/<repo>" ou clonando numa pasta temporária e copiando só as pastas de skill para
   .claude/skills/), mantendo o LICENSE de cada uma. Não copie nada que a licença não permita. Pergunte antes de
   instalar gsap e threejs: só fazem sentido se eu mexo com animação ou 3D na web.
6. Economia de cota: instale o rtk pelo README de https://github.com/rtk-ai/rtk (rode "rtk init -g" no fim) e me
   ofereça a claude-economia-de-cota (https://github.com/viniciuscamp0s/claude-economia-de-cota). O ponytail é
   opcional: só instale se eu pedir, seguindo o veredito de habilidades-dev/docs/03-economia-de-cota.md.
7. Rode o teste: cd habilidades-dev && npm test.
8. Me mostre em até 8 linhas o que ficou instalado e qual habilidade usar em cada etapa (planejar, executar, testar,
   depurar, revisar, segurança, publicar), conforme habilidades-dev/docs/02-guia-das-habilidades.md.
Regras: nada pago sem me dizer o custo antes; segredo (token, senha) eu colo direto no .env, nunca no chat.
```

## O que a instalação faz, passo a passo

| Passo | O que acontece | Quanto custa |
|---|---|---|
| Ferramentas | Node, git, bash, python | 0 (tudo aberto) |
| Skills nossas | `route`, `checagem-de-seguranca`, `checkpoint-de-raciocinio` | 0 |
| Plugins de terceiros | superpowers e os plugins oficiais, pelos comandos `/plugin` de cada autor | 0 |
| Skills de terceiros | baixadas dos repositórios originais (lista e licenças em [`CREDITOS.md`](CREDITOS.md)) | 0 |
| Economia de cota | rtk e, se quiser, claude-economia-de-cota | 0 |
| Teste | `npm test` | alguns segundos |

## Instalação manual (sem IA)

```bash
git clone https://github.com/viniciuscamp0s/habilidades-dev.git
cd habilidades-dev
npm test
mkdir -p ../.claude/skills && cp -r skills/*/ ../.claude/skills/
```

Depois, no Claude Code, cole os comandos `/plugin` do passo 4 do prompt acima. Quer em todos os seus projetos? Copie
as skills para `~/.claude/skills/` em vez de `.claude/skills/`.

## Usar a trava de trabalho pesado

```bash
bash habilidades-dev/ferramentas/trava.sh pesada npm run build
```

Ponha no seu `CLAUDE.md` (ou `AGENTS.md`): "build, suíte inteira de testes, npm ci e deploy rodam sempre por
`bash habilidades-dev/ferramentas/trava.sh pesada <comando>`".

## Atualizar

`cd habilidades-dev && git pull`, depois copie de novo as pastas de `skills/`. Os plugins se atualizam pelo próprio
`/plugin` do Claude Code. O que mudou em cada versão: [`CHANGELOG.md`](CHANGELOG.md).
