// fetch_assets.mjs — baja de Drive las imagenes de una pieza, buscandolas por el nombre de asset.
//
//   node ../_ci/fetch_assets.mjs pieza_4.2.json
//
// Lee cada slide: { asset, drive_id, imagen } y guarda el archivo en `imagen`.
// `drive_id` sale de Airtable (Assets.Link Drive); si falta, busca por nombre de asset en Drive.
// Requiere: GOOGLE_APPLICATION_CREDENTIALS (JSON de la cuenta de servicio). La cuenta solo ve lo que
// Johnny le haya compartido en Drive (rol Lector). Falla de forma visible si falta un asset.

import { GoogleAuth } from 'google-auth-library';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const piezaPath = process.argv[2];
if (!piezaPath) { console.error('Uso: node fetch_assets.mjs <pieza.json>'); process.exit(2); }

const auth = new GoogleAuth({ scopes: ['https://www.googleapis.com/auth/drive.readonly'] });
const client = await auth.getClient();
const API = 'https://www.googleapis.com/drive/v3/files';

async function findByName(name) {
  const q = `name = '${name.replace(/'/g, "\\'")}' and trashed = false`;
  const url = `${API}?q=${encodeURIComponent(q)}&fields=files(id,name,modifiedTime,size,md5Checksum)&orderBy=modifiedTime desc&supportsAllDrives=true&includeItemsFromAllDrives=true&pageSize=10`;
  const res = await client.request({ url });
  return res.data.files || [];
}

async function download(id) {
  const res = await client.request({ url: `${API}/${id}?alt=media&supportsAllDrives=true`, responseType: 'arraybuffer' });
  return Buffer.from(res.data);
}

const pieza = JSON.parse(await readFile(piezaPath, 'utf8'));
const missing = [];
for (const s of pieza.slides) {
  if (!s.asset || !s.imagen) continue;
  // Airtable (Assets.Link Drive) es la fuente: el ID viaja en el JSON de la pieza. Sin ID, busca por nombre.
  const files = s.drive_id ? [{ id: s.drive_id }] : await findByName(s.asset);
  if (!files.length) { console.error(`✗ slide ${s.n}: no encuentro "${s.asset}" en Drive (¿compartido con la cuenta de servicio?)`); missing.push(s.asset); continue; }
  if (files.length > 1) console.warn(`! slide ${s.n}: ${files.length} archivos llamados "${s.asset}"; uso el mas reciente (${files[0].id})`);
  const buf = await download(files[0].id);
  await mkdir(path.dirname(s.imagen), { recursive: true });
  await writeFile(s.imagen, buf);
  console.log(`✓ slide ${s.n}: ${s.asset} -> ${s.imagen} (${(buf.length / 1024).toFixed(0)} KB, id ${files[0].id})`);
}
if (missing.length) { console.error(`Faltan ${missing.length} asset(s). Me detengo.`); process.exit(1); }
