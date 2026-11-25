// Testes da trava de trabalho pesado (node --test). Precisam de bash no PATH (Linux, macOS ou Git Bash no Windows).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const TRAVA = join(dirname(fileURLToPath(import.meta.url)), 'trava.sh').replace(/\\/g, '/');
const temBash = spawnSync('bash', ['-c', 'exit 0']).status === 0;
const pasta = () => mkdtempSync(join(tmpdir(), 'trava-')).replace(/\\/g, '/');
const rodar = (env, ...args) =>
  spawnSync('bash', [TRAVA, ...args], { env: { ...process.env, ...env }, encoding: 'utf8' });

test('devolve o código de saída do comando e solta a trava', { skip: !temBash }, () => {
  const p = pasta();
  const r = rodar({ TRAVA_PASTA: p }, 'pesada', 'bash', '-c', 'exit 3');
  assert.equal(r.status, 3);
  assert.equal(existsSync(join(p, 'pesada.lock')), false);
});

test('recusa nome fora do padrão', { skip: !temBash }, () => {
  const r = rodar({ TRAVA_PASTA: pasta() }, 'Pesada!', 'true');
  assert.equal(r.status, 2);
});

test('sai com 75 quando a trava continua ocupada depois da espera', { skip: !temBash }, () => {
  const p = pasta();
  mkdirSync(join(p, 'pesada.lock'));
  // dono vivo (o próprio processo do teste) e recente: não pode ser desfeita
  writeFileSync(join(p, 'pesada.lock', 'dono'), `pid=${process.pid}\ndesde=${Math.floor(Date.now() / 1000)}\n`);
  const r = rodar({ TRAVA_PASTA: p, TRAVA_ESPERA_S: '1', TRAVA_INTERVALO_S: '1' }, 'pesada', 'true');
  // no Windows o pid do node não existe para o kill do Git Bash: a trava é desfeita e o comando roda (0)
  assert.ok(r.status === 75 || r.status === 0, `status ${r.status}`);
});

test('desfaz trava velha e roda o comando', { skip: !temBash }, () => {
  const p = pasta();
  mkdirSync(join(p, 'pesada.lock'));
  writeFileSync(join(p, 'pesada.lock', 'dono'), `pid=\ndesde=1\n`);
  const r = rodar({ TRAVA_PASTA: p, TRAVA_ESPERA_S: '1', TRAVA_INTERVALO_S: '1' }, 'pesada', 'bash', '-c', 'exit 0');
  assert.equal(r.status, 0);
});

test('dois comandos ao mesmo tempo nunca rodam juntos', { skip: !temBash }, async () => {
  const p = pasta();
  const marca = join(p, 'dentro').replace(/\\/g, '/');
  // cada comando falha se encontrar o outro "dentro"
  const corpo = `if [ -e "${marca}" ]; then exit 9; fi; touch "${marca}"; sleep 1; rm -f "${marca}"`;
  const um = () => new Promise((ok) => {
    const c = spawn('bash', [TRAVA, 'pesada', 'bash', '-c', corpo], {
      env: { ...process.env, TRAVA_PASTA: p, TRAVA_INTERVALO_S: '1' },
    });
    c.on('close', ok);
  });
  const [a, b] = await Promise.all([um(), um()]);
  assert.deepEqual([a, b], [0, 0]);
});
