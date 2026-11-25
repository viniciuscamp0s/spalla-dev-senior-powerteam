// Confere a estrutura das skills deste repositório: cada pasta de skills/ tem um SKILL.md com frontmatter válido,
// o nome bate com a pasta, e todo link relativo dos documentos aponta para um arquivo que existe.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), '..');
const SKILLS = join(RAIZ, 'skills');

test('cada skill tem SKILL.md com name igual à pasta e description', () => {
  const pastas = readdirSync(SKILLS).filter((n) => statSync(join(SKILLS, n)).isDirectory());
  assert.ok(pastas.length >= 3);
  for (const p of pastas) {
    const f = join(SKILLS, p, 'SKILL.md');
    assert.ok(existsSync(f), `${p} sem SKILL.md`);
    const fm = readFileSync(f, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/);
    assert.ok(fm, `${p}: sem frontmatter`);
    assert.match(fm[1], new RegExp(`^name:\\s*${p}\\s*$`, 'm'), `${p}: name diferente da pasta`);
    assert.match(fm[1], /^description:/m, `${p}: sem description`);
  }
});

test('links relativos dos documentos apontam para arquivos que existem', () => {
  const docs = [];
  const andar = (d) => {
    for (const n of readdirSync(d)) {
      if (n.startsWith('.') || n === 'node_modules') continue;
      const c = join(d, n);
      if (statSync(c).isDirectory()) andar(c);
      else if (n.endsWith('.md')) docs.push(c);
    }
  };
  andar(RAIZ);
  const quebrados = [];
  for (const f of docs) {
    const texto = readFileSync(f, 'utf8');
    for (const [, alvo] of texto.matchAll(/\]\(([^)#\s]+)(?:#[^)]*)?\)/g)) {
      if (/^(https?:|mailto:)/.test(alvo)) continue;
      if (!existsSync(resolve(dirname(f), alvo))) quebrados.push(`${f.slice(RAIZ.length + 1)} -> ${alvo}`);
    }
  }
  assert.deepEqual(quebrados, []);
});
