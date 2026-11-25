---
name: checagem-de-seguranca
description: Fase obrigatória no fim de TODA implementação que cria ou muda uma superfície (rota, API, Server Action, página pública, formulário, link com token, webhook, workflow de automação, ferramenta de IA, integração, container, porta, proxy reverso, ferramenta aberta nova), antes de dizer pronto ou publicar. Também a varredura ampla de um sistema inteiro. Use ao fechar qualquer implementação, ao revisar um diff, ou quando pedirem "checagem de segurança", "varredura de segurança", "isso está seguro?". Não é para texto, arte ou documento. Não carregar no início da sessão.
license: MIT
---

# Checagem de segurança

17 riscos de aplicação mais a infraestrutura, cada um com a pergunta certa, onde procurar, como provar e como
corrigir. Os 12 primeiros partem do guia "Vibe coding com segurança" (KipperDev, set/2026); os riscos 13 a 17 (CORS,
clickjacking, enumeração de usuário, dado demais, token na URL) entraram depois, de checagens de pentest. Os exemplos
usam as stacks mais comuns de quem constrói com IA (Next.js, Supabase, Better Auth, PHP, nginx, Docker): troque pela
sua.

## Quando roda

- **No fim de toda implementação que cria ou muda uma superfície**, antes de dizer "pronto" e antes do deploy.
  Bloqueador achado = não publica.
- Não roda para texto, arte, documento ou mudança sem código.
- É a última fase, nunca a primeira leitura da sessão (gastaria contexto à toa).

| Tamanho da mudança | O que fazer |
|---|---|
| Pequena (um arquivo, sem entrada nova de fora) | Passo 1 e só as linhas do passo 2 que a mudança toca |
| Rota, formulário, link, webhook, IA, dinheiro ou infra nova | Passos 1, 2 e 3 sobre o diff inteiro |
| Sistema novo, ou pediram varredura | Varredura ampla (fim deste arquivo) |

## Passo 1. Varredor (custo zero de token)

Na raiz do repositório da mudança:

```
python <pasta-desta-skill>/scripts/varrer.py              # diff contra HEAD + arquivos novos
python <pasta-desta-skill>/scripts/varrer.py --base main  # tudo que mudou desde main
python <pasta-desta-skill>/scripts/varrer.py --caminho app/api
```

No Windows, `py -I` no lugar de `python`. Cada sinal se confirma lendo o fluxo: de onde vem o dado e quem o controla.
**Sinal não é falha, e nenhum sinal não é prova de segurança.**

## Passo 2. O que o varredor não responde

Para cada superfície tocada, responda com evidência (`arquivo:linha`):

| # | Risco | A pergunta |
|---|---|---|
| 01 | Segredo no front | Algum segredo chega ao navegador (bundle, HTML, resposta, source map)? Next: `NEXT_PUBLIC_` só para URL e chave pública (anon); módulo com chave é `server-only`. PHP e estático: nada de token no HTML/JS, e arquivo de dado ou de chave nunca servível pelo servidor web (bloqueie JSON de estado, `*.sqlite`, `*.key`, pastas de dado). Segredo mora num lugar só (`.env` fora do git) |
| 02 | Entrada sem validação | Toda entrada de fora passa por schema no servidor (Zod ou equivalente), com tamanho máximo, só os campos previstos e sem espalhar o corpo no insert? No PHP: tipo, tamanho e lista de campos antes de gravar |
| 03 | SQL injection | Valor sempre por parâmetro (query builder, cliente oficial); filtro com texto do usuário só pela função de escape do cliente; `format()` de migration com `%L`/`%I`; coluna e ordenação vindas de lista fixa |
| 04 | Prompt injection | O que a IA lê de fora (mensagem de usuário, nome de produto, e-mail recebido) pode fazê-la agir sobre dado de outra pessoa? Ferramenta usa o contato e a organização **da conversa**, nunca id ou telefone escolhido pelo modelo; saída da IA nunca vira destino, URL ou comando; texto de um cliente nunca entra no prompt de outro; teto de custo por conversa e por conta |
| 05 | XSS | Dado de terceiro vira texto, nunca HTML: React escapa, `textContent` no lugar de `innerHTML`, `htmlspecialchars` no PHP; nada de `dangerouslySetInnerHTML` com dado |
| 06 | IDOR/BOLA | Toda leitura, edição e exclusão filtra pela identidade da sessão e pela organização (RLS; com cliente de serviço, a própria ação confere o dono). Link público: token aleatório de 128 bits ou mais, guardado como hash, com validade, nunca chave previsível (`cliente_pagina_2026`) |
| 07 | SSRF | O servidor só busca destino fixo (mapa no código) ou de lista permitida, com `redirect: 'manual'`, timeout e limite de tamanho; URL vinda de payload nunca é buscada direto |
| 08 | Senha | Só provedor de autenticação pronto (Supabase Auth, Better Auth com scrypt, Auth.js...). Nunca hash próprio, nunca senha em log ou resposta |
| 09 | Abuso e DoS | Rota pública e rota que gasta IA, mensagem ou pagamento têm limite por IP, número ou conversa **e** teto global. Limitador em memória zera no deploy: o que importa conta no banco |
| 10 | Rota administrativa | Nega por padrão; segredo comparado em tempo constante (`timingSafeEqual`, `hash_equals`) antes de ler o corpo; papel vem da sessão, nunca do corpo; nada de rota de teste, mock ou debug em produção; painel administrativo (automação, hospedagem) com 2FA |
| 11 | Bot em formulário | Formulário público tem honeypot e limite por IP no mínimo; o que dispara mensagem ou IA ganha desafio validado no servidor (Turnstile, hCaptcha) |
| 12 | Erro que vaza | Ao cliente, frase genérica; o detalhe vai para o log, sem token, telefone ou corpo inteiro; PHP com `display_errors=0` |
| 13 | CORS refletindo a origem | O servidor devolve `Access-Control-Allow-Origin` copiando o `Origin` da requisição, aceita `null`, ou junta `*` com `Allow-Credentials: true`? **Procurar:** `rg -n -e "Access-Control-Allow" -e "cors\(" .` **Prova:** `curl -si -H "Origin: https://evil.example" <URL>` numa rota que devolve dado de sessão; `evil.example` não pode voltar em nenhum cabeçalho `Access-Control-*`. **Corrigir:** o padrão é não mandar cabeçalho CORS. Rota que precisa abrir usa lista fixa de origens comparada por igualdade exata (nunca `endsWith`, `includes` ou regex solta), com `Vary: Origin`, e `Allow-Credentials` só para origem da lista. Webhook continua protegido pelo segredo do risco 10; CORS não o substitui |
| 14 | Clickjacking | Toda página HTML, em especial a que tem botão de aprovar, pagar, enviar ou apagar, proíbe ser emoldurada por outro domínio? **Prova:** `curl -sI <URL>` e ler `content-security-policy` e `x-frame-options`; sem nenhum dos dois, qualquer site a emoldura com um iframe transparente e leva o clique. **Corrigir (Next):** `headers()` do `next.config` em `/:path*` com `Content-Security-Policy: frame-ancestors 'none'` e `X-Frame-Options: DENY`. nginx: `add_header`. Página que deve ser emoldurada abre só a rota dela, com `frame-ancestors` listando os domínios exatos, nunca `*` |
| 15 | Enumeração de usuário | Login, "esqueci a senha" e cadastro respondem igual (texto, status, redirecionamento e tempo) para e-mail que existe e que não existe? **Prova:** duas chamadas iguais, um e-mail real e um inventado, comparando corpo, status e `curl -s -o /dev/null -w "%{http_code} %{time_total}\n"`. **Corrigir:** mesma frase e mesmo status ("Se o e-mail existir, enviamos o link"; "E-mail ou senha incorretos"); no login sem usuário, comparar contra um hash falso para o tempo não denunciar; e-mail de recuperação enviado fora do caminho da resposta; cadastro com e-mail existente responde como sucesso e avisa a pessoa por e-mail. Limite por IP e por e-mail (09) vale à parte |
| 16 | Resposta com dado demais | Rota, ação ou página devolve a linha inteira do banco (`select *`, `returning *`, usuário inteiro) e deixa o front esconder? Não é o 06 (de quem é a linha): aqui é **quais colunas** saem. **Procurar:** `rg -n -e "select \*" -e "returning \*" -e "selectAll\(" -e "\.select\(\)" .` e espalhamento de linha no retorno (`...row`, `...user`). **Prova:** abrir a resposta crua e procurar `password`, `hash`, `token`, `secret`, e-mail ou telefone de outra pessoa, custo e campo interno. **Corrigir:** lista fixa de colunas em cada consulta; objeto de resposta montado à mão; componente de servidor passa ao cliente só os campos usados (o que cruza vai para o HTML) |
| 17 | Token ou segredo na URL | Token, chave, senha ou id de sessão viaja na query string ou no caminho? A URL vai para o histórico, o log do proxy, o `Referer`, o analytics e o print. **Procurar:** `rg -n -e "[?&]token=" -e "[?&]key=" -e "[?&]secret=" -e "req\.query" -e "_GET\[" .` **Corrigir:** segredo em cabeçalho (`Authorization`), cookie HttpOnly ou corpo de POST. Link que precisa do token na URL (convite, redefinição de senha, aprovação) segue o 06 (128 bits, hash, validade curta, uso único), e a página troca o token por sessão e limpa a barra (`history.replaceState`), com `Referrer-Policy: no-referrer`. Logout revoga a sessão no servidor e troca de senha derruba as abertas; **prova:** copiar o cookie, sair, reusar e esperar 401 |
| — | Infra | Docker publica porta por fora do firewall do sistema (o ufw não vê): porta só abre pela chain `DOCKER-USER` ou pelo proxy reverso. Imagem com versão fixada (nunca `:latest`). Versão sem alerta aberto (`gh api repos/<org>/<repo>/security-advisories`). Ferramenta aberta nova passa por checklist (licença, manutenção, permissões, telemetria, versão fixada) antes de entrar |

## Passo 3. Prova

- Cada achado com o fluxo, `arquivo:linha`, a condição para explorar e o impacto, marcado como confirmado, suspeita
  ou não verificado.
- Teste negativo e positivo: entrada inválida recusada e válida aceita; conta A não lê nem altera B; excesso de
  tentativas dá 429; token reaproveitado é negado.
- Nunca teste de carga em produção, nunca alterar dado real. Em produção, só GET de leitura no seu próprio domínio.

## Achou falha

Fecha na hora, inteira: vulnerabilidade que está no seu controle passa na frente de tudo e nunca vira "recomendo
trocar quando der". Procure o mesmo defeito nos moldes e em todas as cópias (outro sistema que nasceu do mesmo
template quase sempre tem o mesmo buraco). Segredo exposto se troca, e toda cópia dele junto.

## Como entrega

Na mensagem final da implementação, uma linha quando está limpo:
`Segurança: varredor sem sinal novo; 02, 06 e 09 conferidos (arquivo:linha); sem bloqueador.`
Com achado, tabela `risco | evidência | severidade | correção | teste`, separando bloqueador de publicação, melhoria e
dependência externa. **Nunca "está seguro" só porque os testes passaram.**

## Varredura ampla

Um subagente por sistema, num modelo intermediário, somente leitura, sem rede e sem abrir `.env`, devolvendo tabela
de até 20 linhas; o modelo principal confirma cada achado antes de agir. Prompt-base em
`referencias/prompt-varredura.md`. Infra ao vivo: regras do firewall, portas abertas (`ss -tlnH`), chain
`DOCKER-USER`, GET nos caminhos que o subagente listar e a versão de cada imagem contra os alertas oficiais. Registre
a varredura com data num arquivo do próprio repositório, para a próxima comparar.
