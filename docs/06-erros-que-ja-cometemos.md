# Erros que já cometemos (e a regra que cada um virou)

Cada linha é um erro real de desenvolvimento com IA, nos nossos sistemas, e a trava que passou a valer. Leia antes de
publicar qualquer coisa: é mais barato aprender aqui do que em produção.

## Publicação e produção

| Erro | Regra |
|---|---|
| Sessões diziam "já corrigido" por 12 dias; produção rodava o código antigo porque ninguém publicou | Editado não é entregue. O que vale é a versão publicada: confira o que roda em produção, não o arquivo |
| Uma frente foi dada como "nada a publicar" porque o branch estava pronto; a imagem no ar estava atrás da main | "Já publicado" só se confirma pelo que roda em produção, nunca pelo branch |
| Uma sessão paralela publicou uma versão mais antiga por cima da nova | Antes de publicar, confira a versão em produção e não sobrescreva o deploy de outra frente |
| O build reaproveitou o cache de uma rota apagada e o typecheck quebrou | Ao remover rota ou página, limpe o cache de build antes de publicar |
| Container em duas redes: o proxy roteou pela errada, o health deu timeout e a primeira hipótese foi falta de memória | Diagnostique pelo roteamento e pelos logs antes de culpar recurso |
| Health check que só devolvia 200 não percebia integração fora do ar | Health de produção cobre banco, filas, integrações e a rota real |
| Rollback manual dependia de alguém lembrar a imagem anterior | Todo deploy guarda a imagem anterior e tem volta automática testada |
| Migration aplicada em produção sem o arquivo no repositório; o deploy seguinte recusou | Migration aplicada está commitada, e um verificador arquivo × banco é portão de deploy |
| Migration de separação de dados apagou linhas em dezenas de tabelas | Migration destrutiva só com backup, restauração de teste e contagem conferida; prefira migration aditiva |
| Documento dizia que um serviço estava fora do ar desde certa data; o container estava de pé havia 31 horas | Confira o estado real (processos, containers) antes de confiar em documento |

## Testes e verificação

| Erro | Regra |
|---|---|
| Teste de inicialização estourou o tempo porque outra bateria rodava na mesma máquina; isolado, passou em segundos | Antes de culpar o código, rode isolado; nunca publique com bateria pesada concorrente |
| Teste com tempo justo passava sozinho e falhava sob carga | Teste sensível a tempo ganha folga e não entra no portão sem isolamento |
| A revisão do diff pegou falhas que os testes não cobriam (ordem perdida ao gravar, número lido como texto) | Revisão do diff inteiro antes de publicar, além dos testes |
| A conferência visual foi feita numa camada isolada e escondeu o defeito da composição final | Confira o resultado composto, nunca a parte |
| "Feito" relatado sem ninguém ter visto a tela logada | O relato lista o que não foi verificado, em vez de omitir |
| Um subagente declarou o arquivo trocado; os bytes eram os da versão antiga | Confira por hash, tamanho ou commit no artefato servido, nunca pela declaração do agente |

## Sessões, cota e contexto

| Erro | Regra |
|---|---|
| Quase um quarto da cota da semana foi reescrevendo contexto de sessões acordadas depois de o cache vencer | Sessão que espera acorda em menos de 1 hora ou encerra com passagem |
| Sessão grande retomada depois de cair perdia qualidade e custava caro | Acima de um limite de contexto, sessão nova com resumo de passagem, nunca retomada |
| Sessões pararam no meio da madrugada sem ninguém ver | Sessão longa é vigiada e retomada do ponto onde parou, até o fim |
| A cota acabou no meio de uma publicação e deixou a etapa pela metade | Planeje pela cota; ao parar, grave o estado e retome pelo estado real |
| 57% dos tokens de subagente da semana eram do modelo mais caro, a maioria lendo | Subagente leva o modelo na chamada: barato para ler, forte só para julgar |
| Regras carregadas em toda sessão consumiam cota a cada abertura | Regra curta com ponteiro; o porquê fica em arquivo lido sob demanda |
| A sessão mais cara terminou pedindo à pessoa para abrir outra sessão e colar um prompt | Organizar sessões e escolher o modelo é trabalho do orquestrador, nunca da pessoa |

## Execução paralela e memória do computador

| Erro | Regra |
|---|---|
| Cinco sessões rodando testes ao mesmo tempo num PC de 16 GB derrubaram umas às outras o dia inteiro | Trabalho pesado passa pela [trava](../ferramentas/trava.sh), um por vez no computador |
| Frentes disputavam a mesma trava sem ordem de chegada; uma esperou horas | Fila com ordem de chegada e teto de espera por chamada |
| Falta de memória derrubou processos de outra frente no meio de uma rodada | Meça a memória livre antes de abrir frente pesada |
| Três chamadas simultâneas a um serviço externo voltaram com erro; uma por vez era mais rápida no total | Limite de concorrência por serviço externo |
| Duas sessões abertas na mesma pasta, e o trabalho de uma sumiu | Uma pasta, uma sessão: confira se já há sessão viva antes de abrir |
| Sessões e worktrees de entregas fechadas se acumularam e pesaram na máquina | Quem abre fecha; a limpeza só remove o que já foi integrado |
| Um filtro amplo de limpeza apagou transcrições de sessões antigas | Limpeza só por caminho exato, nunca por padrão de nome |

## Segredos e segurança

| Erro | Regra |
|---|---|
| Um token colado em texto livre foi repetido no chat durante a explicação | Nunca ecoar valor de segredo; segredo vai direto no `.env`, nunca no chat |
| Um atalho de terminal imprimiu uma chave dentro de uma mensagem de erro | Nunca imprima variáveis de ambiente; vazamento se resolve com troca da chave no mesmo dia |
| A troca de uma chave vazada deixou para trás outras do mesmo vazamento | Achou um vazamento: varra tudo do mesmo tipo e troque o conjunto inteiro, na hora |
| Cópias do `.env` espalhadas em worktrees e backups | Um mapa único de onde cada segredo mora, com um comando que propaga a troca |
| Rota de entrada lia o corpo antes de checar o segredo | Segredo comparado em tempo constante antes de ler o corpo; recusa sem processar |
| Repositório público quase saiu com termos internos | Varredura de privacidade antes do commit e de novo no `pre-push` |
| Autorização dada no chat não destravou ação com custo no modo automático | Autorização no chat não substitui a permissão configurada; ação com dinheiro pede o sim explícito |

## Git e repositório

| Erro | Regra |
|---|---|
| Imagens entraram no git e inflaram o repositório a 75% do tamanho | Git recebe texto, código e documento; o pre-commit recusa imagem sem uso e arquivo grande |
| Um plano de trabalho foi varrido para dentro do repositório pelo commit de outra sessão | Commit só dos seus arquivos, nunca `git add -A` em pasta compartilhada; plano temporário no `.gitignore` |
| Reescrita de histórico feita com lista de caminhos errada | Em reescrita, decida arquivo a arquivo por regra, nunca por lista colada |
| Sincronização travou porque o histórico divergiu, e alguém contornou com cópia direta | Divergência de histórico se investiga; nunca contorne sincronização com cópia à mão |

## Delegação a outro modelo e a subagentes

| Erro | Regra |
|---|---|
| O executor parou por limite de cota no meio da rodada e deixou a entrega sem testes | Quem completa aplica o mesmo rigor de teste e revisão do diff |
| Código escrito por outro modelo tinha erro de regra de negócio que só o teste pegou | Código delegado passa pela mesma revisão e pelos mesmos testes |
| Um "modelo lotado" foi tratado como "sem cota" por causa de uma anotação antiga | Confira a mensagem de erro de hoje, nunca a de ontem |
| Delegação sem escopo mexeu em arquivo que não era da tarefa | Delegue com objetivo, arquivos permitidos e saída verificável |

## Documentação e regras

| Erro | Regra |
|---|---|
| A lista de clientes existia em três fluxos com três formatos; um cancelado seguiu monitorado por semanas | Toda regra tem um lugar só; as cópias são geradas ou apontam para lá |
| Uma regra aposentada continuou viva em três arquivos e foi herdada por uma skill nova | Ao aposentar uma regra, cace todas as cópias |
| Uma regra permanente ficou só no diário, onde as sessões não a leem | Regra permanente vai ao documento que as sessões carregam (ver [`checkpoint-de-raciocinio`](../skills/checkpoint-de-raciocinio/SKILL.md)) |
