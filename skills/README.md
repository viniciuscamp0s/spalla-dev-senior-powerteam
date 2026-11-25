# As nossas skills

Criadas por nós, em versão universal (sem nada do nosso negócio dentro). Instale copiando cada pasta para
`.claude/skills/` do seu projeto, ou `~/.claude/skills/` para valer em todos.

| Skill | Função | Como chamar |
|---|---|---|
| [`route`](route/SKILL.md) | Executar com outro modelo: o Claude planeja e revisa, o Codex escreve o código | `/route "<tarefa>"` |
| [`checagem-de-seguranca`](checagem-de-seguranca/SKILL.md) | Segurança: 17 riscos + infra, com varredor sem IA (`scripts/varrer.py`) | "checagem de segurança" no fim de toda implementação |
| [`checkpoint-de-raciocinio`](checkpoint-de-raciocinio/SKILL.md) | Orquestrar: transforma um "sempre/nunca" em regra permanente no arquivo certo | `/checkpoint-de-raciocinio` ou "aprenda esse modo de pensar" |

As de terceiros (superpowers, plugins oficiais, impeccable e as demais) não são copiadas aqui: a instalação baixa
cada uma do repositório original. Lista, autores e licenças em [`../CREDITOS.md`](../CREDITOS.md); quando usar cada
uma em [`../docs/02-guia-das-habilidades.md`](../docs/02-guia-das-habilidades.md).
