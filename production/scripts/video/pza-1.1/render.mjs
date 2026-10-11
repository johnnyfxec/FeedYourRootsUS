// render.mjs — arma el video de PZA_1.1 con Clipkit (local, gratis) en una o varias variantes
//
//   node render.mjs                      -> renderiza A y B-e14
//   node render.mjs B-e18 B-e10-nm       -> variantes concretas
//   node render.mjs --dry B-e14          -> solo escribe el JSON de Clipkit en salida/, sin renderizar
//
// Variantes:  A = subtítulo nativo de Clipkit (palabra activa resaltada)
//             B = una palabra a la vez, énfasis más grande y dorado
//   modificadores: -e14 (énfasis 1.4x; -e10, -e18...)  -nm (sin movimiento de cámara)  -up (MAYÚSCULAS)

import http from 'node:http';
import { createReadStream, existsSync, statSync, readFileSync } from 'node:fs';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { buildSource } from './lib.mjs';

const ROOT = path.resolve('.');
const args = process.argv.slice(2);
const dry = args.includes('--dry');
const variants = args.filter((a) => !a.startsWith('--'));
if (!variants.length) variants.push('A', 'B-e14');

const MIME = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.ttf': 'font/ttf', '.otf': 'font/otf' };

function serve() {
  const srv = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(ROOT) || !existsSync(p) || statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream', 'Access-Control-Allow-Origin': '*' });
    createReadStream(p).pipe(res);
  });
  return new Promise((r) => srv.listen(0, '127.0.0.1', () => r({ srv, base: `http://127.0.0.1:${srv.address().port}` })));
}

function pngSize(file) {
  const b = readFileSync(file);
  if (b.toString('ascii', 1, 4) !== 'PNG') return null;
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

async function main() {
  const cfg = JSON.parse(await readFile('pieza_1.1.json', 'utf-8'));
  if (!existsSync('build/timings.json')) throw new Error('Falta build/timings.json — corre primero: node tts.mjs');
  const timings = JSON.parse(await readFile('build/timings.json', 'utf-8'));

  // revisar imágenes
  let bad = false;
  for (const s of cfg.slides) {
    if (!existsSync(s.imagen)) { console.error(`✗ Falta la imagen del slide ${s.n}: ${s.imagen}  (${s.asset})`); bad = true; continue; }
    const sz = pngSize(s.imagen);
    if (sz) {
      const ratio = sz.w / sz.h;
      const ok = Math.abs(ratio - 9 / 16) < 0.01;
      console.log(`  slide ${s.n}: ${sz.w}x${sz.h}${ok ? '' : '  ⚠ no es 9:16 — se recortará con fit=cover'}`);
    }
  }
  if (bad) process.exit(1);

  const fontOk = cfg.fuente_subtitulos && existsSync(cfg.fuente_subtitulos.file);
  if (!fontOk) console.log(`⚠ No encontré ${cfg.fuente_subtitulos?.file}; los subtítulos usarán la fuente por defecto (Inter).`);

  await mkdir('salida', { recursive: true });
  const { srv, base } = await serve();
  const { render } = dry ? {} : await import('@clipkit/renderer');

  try {
    for (const variant of variants) {
      const name = `${cfg.pieza_id}__sub${variant}`;
      const source = buildSource({ cfg, timings, variant, base, fontOk });
      await writeFile(`salida/${name}.json`, JSON.stringify(source, null, 2));
      if (dry) { console.log(`✓ ${name}.json (${source.duration}s, ${source.elements.length} elementos)`); continue; }
      console.log(`\nRenderizando ${name} (${source.duration}s)...`);
      const t0 = Date.now();
      const result = await render({
        source,
        backend: 'auto',
        onProgress: (f, total) => process.stdout.write(`\r  frame ${f}/${total}`),
      });
      process.stdout.write('\n');
      await writeFile(`salida/${name}.mp4`, result.buffer);
      console.log(`  ✓ salida/${name}.mp4 — ${result.durationSec}s de video, tardó ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  } finally {
    srv.close();
  }
}

main().catch((e) => { console.error('Error:', e.message); process.exit(1); });
