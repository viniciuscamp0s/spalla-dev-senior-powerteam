"""Varredor de sinais de risco da checagem de segurança (custo zero de token).

Aponta, por risco do padrão (01 a 12 + infra; 13 a 17 pela checklist do SKILL.md), as linhas que pedem conferência
humana ou da IA. Não prova que algo é seguro: só acha o que é procurável por
texto. O resto é a checklist manual do SKILL.md.

Uso (na raiz de qualquer repositório git):
  python varrer.py                 # mudanças ainda não commitadas (diff contra HEAD)
  python varrer.py --base main     # tudo que mudou desde main
  python varrer.py --caminho app/  # pasta ou arquivo inteiro
No Windows, `py` no lugar de `python`.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

EXTS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".php", ".py", ".html", ".sql",
        ".json", ".yml", ".yaml", ".conf", ".sh", ".gs", ".env"}
IGNORAR = re.compile(r"(node_modules|\.next|dist|build|_BACKUP-GIT|/tmp/|\.test\.|\.spec\.|"
                     r"/tests?/|package-lock|varrer\.py)")

# (risco, descrição, regex). Uma linha pode casar mais de uma regra.
REGRAS = [
    ("01", "chave privada em variável pública do front",
     r"(NEXT_PUBLIC|VITE|PUBLIC)_[A-Z0-9_]*(SECRET|PRIVATE|SERVICE_ROLE|TOKEN|PASSWORD|API_KEY)"),
    ("01", "valor com cara de segredo escrito no código",
     r"(sk-[A-Za-z0-9_-]{20,}|gsk_[A-Za-z0-9]{20,}|EAA[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|"
     r"-----BEGIN [A-Z ]*PRIVATE KEY|xox[bp]-[0-9A-Za-z-]{20,})"),
    ("01", "cliente sem RLS / chave de serviço (conferir que não vai ao navegador)",
     r"(createServiceClient|SUPABASE_SERVICE_ROLE|service_role)"),
    ("02", "corpo da requisição usado sem schema (conferir Zod/validação no servidor)",
     r"(\.\.\.\s*(req\.body|body|await\s+req(uest)?\.json\(\))|file_put_contents\([^;]*\$_(GET|POST|REQUEST))"),
    ("03", "SQL ou filtro montado com interpolação",
     r"(\.(or|filter|textSearch)\(\s*`[^`]*\$\{|EXECUTE\s+format\([^)]*%s|sql\.raw|\.unsafe\(|"
     r"\$queryRawUnsafe|\$executeRawUnsafe|->query\([^)]*\$_|SELECT[^\"']*\"\s*\.\s*\$)"),
    ("04", "ferramenta de IA recebe id/telefone escolhido pelo modelo (escopar pelo contexto)",
     r"(contactId|dealId|userId|organizationId|organization_id|phone|telefone)\s*:\s*z\."),
    ("05", "HTML montado a partir de dado (XSS)",
     r"(dangerouslySetInnerHTML|\.innerHTML\s*[+]?=|insertAdjacentHTML|document\.write\(|v-html|"
     r"echo\s+\$_(GET|POST|REQUEST))"),
    ("07", "requisição do servidor para URL vinda de entrada (SSRF)",
     r"(fetch|axios\.(get|post)|got|file_get_contents|curl_init)\(\s*\$?(req|request|body|input|params|payload|data|url|link)\b"),
    ("08", "hash fraco perto de senha",
     r"(senha|password|passwd).{0,60}(md5|sha1|sha256|createHash)|(md5|sha1)\(.{0,40}(senha|password)"),
    ("10", "rota administrativa, de depuração ou de teste",
     r"[\"'/](admin|debug|test|internal|cron|dev)[/\"'](?!null)"),
    ("12", "erro técnico devolvido ao cliente",
     r"((json|Response|send|echo|NextResponse\.json)\(.{0,80}(error|err|e)\.(message|stack)|"
     r"display_errors\s*[=,]\s*['\"]?(1|on)|var_dump\(|print_r\()"),
    ("infra", "porta publicada para a internet (Docker ignora o ufw)",
     r"(^\s*-\s*[\"']?\d{2,5}:\d{2,5}|0\.0\.0\.0:\d+|--publish|-p\s+\d+:\d+)"),
    ("infra", "imagem sem versão fixada",
     r"(image:\s*[\w./-]+(:latest)?\s*$|FROM\s+[\w./-]+:latest)"),
    ("infra", "listagem de pasta ou arquivo de dado servido",
     r"(autoindex\s+on|state\.json|\.sqlite|\.key\b)"),
]
COMPILADAS = [(r, d, re.compile(p, re.IGNORECASE)) for r, d, p in REGRAS]
MASCARA = re.compile(r"([A-Za-z0-9_\-]{4})[A-Za-z0-9_\-]{12,}")


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("git falhou: " + r.stderr.strip())
    return r.stdout


def linhas_do_diff(base):
    """(arquivo, número, texto) de cada linha adicionada no diff."""
    alvo = [base] if base else ["HEAD"]
    saida = git("diff", "--unified=0", "--no-color", *alvo)
    novos = git("ls-files", "--others", "--exclude-standard").splitlines()
    arq, n = None, 0
    for ln in saida.splitlines():
        if ln.startswith("+++ "):
            arq = ln[6:] if ln.startswith("+++ b/") else None
        elif ln.startswith("@@"):
            m = re.search(r"\+(\d+)", ln)
            n = int(m.group(1)) if m else 0
        elif ln.startswith("+") and arq:
            yield arq, n, ln[1:]
            n += 1
    for arq in novos:
        yield from linhas_do_arquivo(Path(arq))


def linhas_do_arquivo(p):
    if p.is_dir():
        for f in sorted(p.rglob("*")):
            yield from linhas_do_arquivo(f)
        return
    if not p.is_file() or p.suffix.lower() not in EXTS or p.stat().st_size > 2_000_000:
        return
    try:
        texto = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for i, ln in enumerate(texto.splitlines(), 1):
        yield str(p).replace("\\", "/"), i, ln


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="ramo ou commit de comparação (padrão: HEAD)")
    ap.add_argument("--caminho", help="pasta ou arquivo inteiro, em vez do diff")
    a = ap.parse_args()
    fonte = linhas_do_arquivo(Path(a.caminho)) if a.caminho else linhas_do_diff(a.base)
    achados = {}
    for arq, n, ln in fonte:
        if IGNORAR.search(arq) or len(ln) > 400:
            continue
        for risco, desc, rx in COMPILADAS:
            if rx.search(ln):
                trecho = MASCARA.sub(r"\1…", ln.strip())[:140]
                achados.setdefault((risco, desc), []).append("%s:%d  %s" % (arq, n, trecho))
    if not achados:
        print("Nenhum sinal procurável. Siga a checklist manual do SKILL.md (06, 09, 11 e o resto).")
        return 0
    for (risco, desc), itens in sorted(achados.items()):
        print("\n[%s] %s (%d)" % (risco, desc, len(itens)))
        for it in itens[:15]:
            print("   " + it)
        if len(itens) > 15:
            print("   … mais %d" % (len(itens) - 15))
    print("\nSinal não é falha: confirme cada um lendo o fluxo (de onde vem o dado, quem controla).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
