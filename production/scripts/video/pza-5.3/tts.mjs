// tts.mjs — genera la voz (un WAV por slide) + tiempos de cada palabra, para PZA_5.3
//
//   node tts.mjs --probe            -> prueba varias voces: ¿devuelven marcas de palabra? + WAV de muestra para escucharlas
//   node tts.mjs                    -> genera audio de todos los slides con la voz de pieza_5.3.json
//   node tts.mjs --voice en-US-Neural2-H   -> igual pero con otra voz
//
// Requiere: GOOGLE_APPLICATION_CREDENTIALS apuntando al JSON de credenciales.

import textToSpeech from '@google-cloud/text-to-speech';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { tokenize, toSSML, wavInfo } from './lib.mjs';
import { withRetry } from '../_ci/retry.mjs';

const client = new textToSpeech.v1beta1.TextToSpeechClient();
const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };

async function synth({ ssml, text, name, languageCode = name.split('-').slice(0, 2).join('-'), speakingRate = 1.0, pitch = 0 }) {
  const [res] = await withRetry(() => client.synthesizeSpeech({
    input: ssml ? { ssml } : { text },
    voice: { languageCode, name },
    audioConfig: { audioEncoding: 'LINEAR16', sampleRateHertz: 24000, speakingRate, ...(pitch ? { pitch } : {}) },
    ...(ssml ? { enableTimePointing: ['SSML_MARK'] } : {}),
  }), { label: `TTS ${name}` });
  return { audio: Buffer.from(res.audioContent), timepoints: res.timepoints || [] };
}

async function probe() {
  const voices = [
    'en-GB-Neural2-B', 'en-GB-Neural2-D', 'en-GB-Neural2-O',
    'en-GB-Wavenet-B', 'en-GB-Wavenet-D',
    'en-GB-Standard-B', 'en-GB-Standard-D',
    'en-GB-Studio-B',
    'en-GB-Chirp3-HD-Charon', 'en-GB-Chirp3-HD-Fenrir', 'en-GB-Chirp3-HD-Orus', 'en-GB-Chirp3-HD-Puck',
    'en-US-Chirp3-HD-Charon',
  ];
  const text = "Number *five*: fill the seed tray. Soil doesn't care how small the hands are.";
  const tokens = tokenize(text);
  const ssml = toSSML(tokens);
  await mkdir('build/probe', { recursive: true });
  console.log('Texto de prueba: ' + tokens.length + ' palabras, velocidad 0.95');
  console.log('VOZ                         MARCAS  DURACION  ESTADO');
  for (const name of voices) {
    const hd = /Chirp|Journey|Studio/.test(name);
    const base = { name, speakingRate: 0.95, pitch: hd ? 0 : -2 };
    const label = name.padEnd(27);
    try {
      const { audio, timepoints } = await synth({ ssml, ...base });
      const d = wavInfo(audio).duration;
      await writeFile('build/probe/' + name + '.wav', audio);
      const ok = timepoints.length === tokens.length;
      console.log(label + ' ' + String(timepoints.length).padStart(3) + '/' + tokens.length + '   ' + d.toFixed(2).padStart(5) + 's   ' + (ok ? 'OK - con marcas de palabra' : 'sin marcas completas'));
    } catch (e1) {
      try {
        const plain = tokens.map((t) => t.speak).join(' ');
        const { audio } = await synth({ text: plain, ...base });
        const d = wavInfo(audio).duration;
        await writeFile('build/probe/' + name + '_SIN-MARCAS.wav', audio);
        console.log(label + '   -        ' + d.toFixed(2).padStart(5) + 's   SIN marcas (solo muestra de voz)');
      } catch (e2) {
        console.log(label + '   -          -     ERROR: ' + String(e2.message).split('\n')[0].slice(0, 80));
      }
    }
  }
  console.log('\nWAV en build/probe/. Los que dicen OK sirven tal cual para subtitulos palabra por palabra.');
}

async function deep() {
  const text = "Number five: fill the seed tray. Soil doesn't care how small the hands are.";
  await mkdir('build/probe-deep', { recursive: true });
  const male = [];
  for (const lang of ['en-US', 'en-GB', 'en-AU']) {
    const [res] = await client.listVoices({ languageCode: lang });
    for (const v of res.voices) if (v.ssmlGender === 'MALE') male.push(v.name);
  }
  male.sort();
  const groups = {};
  for (const n of male) {
    const g = n.replace(/^en-[A-Z]{2}-/, '').replace(/-[A-Za-z0-9]+$/, '');
    (groups[g] = groups[g] || []).push(n.replace(/^en-/, ''));
  }
  console.log('VOCES MASCULINAS DISPONIBLES (en-US / en-GB / en-AU):');
  for (const g of Object.keys(groups)) console.log('  ' + g + ' (' + groups[g].length + '): ' + groups[g].join(', '));
  const jobs = [];
  for (const n of male) if (/Chirp3-HD/.test(n) && /^en-(US|GB)-/.test(n)) jobs.push({ name: n, pitch: 0, file: n });
  for (const n of ['en-US-Neural2-J', 'en-GB-Wavenet-D', 'en-GB-Standard-D', 'en-GB-Neural2-O', 'en-GB-Neural2-D']) {
    for (const p of [-4, -8]) jobs.push({ name: n, pitch: p, file: n + '_pitch' + p });
  }
  console.log('\nGenerando ' + jobs.length + ' muestras en build/probe-deep/ ...');
  for (const j of jobs) {
    try {
      const audioConfig = { audioEncoding: 'LINEAR16', sampleRateHertz: 24000, speakingRate: 0.95 };
      if (j.pitch) audioConfig.pitch = j.pitch;
      const [res] = await withRetry(() => client.synthesizeSpeech({
        input: { text },
        voice: { languageCode: j.name.split('-').slice(0, 2).join('-'), name: j.name },
        audioConfig,
      }), { label: `TTS ${j.name}` });
      await writeFile('build/probe-deep/' + j.file + '.wav', Buffer.from(res.audioContent));
      console.log('  OK    ' + j.file);
    } catch (e) {
      console.log('  ERROR ' + j.file + ' - ' + String(e.message).split('\n')[0].slice(0, 80));
    }
  }
  console.log('\nListo. Escucha build/probe-deep/ y dime tus 2-3 favoritas.');
}

async function generate() {
  const cfg = JSON.parse(await readFile('pieza_5.3.json', 'utf-8'));
  const voice = { ...cfg.voz, ...(opt('--voice') ? { name: opt('--voice') } : {}), ...(opt('--rate') ? { speakingRate: +opt('--rate') } : {}), ...(opt('--pitch') ? { pitch: +opt('--pitch') } : {}) };
  await mkdir('build/audio', { recursive: true });
  const out = { pieza_id: cfg.pieza_id, voz: voice, slides: [] };
  let totalSecs = 0;

  for (const s of cfg.slides) {
    const tokens = tokenize(s.texto_narrado);
    const ssml = toSSML(tokens);
    const { audio, timepoints } = await synth({ ssml, ...voice });
    const info = wavInfo(audio);
    const file = `build/audio/slide_${s.n}.wav`;
    await writeFile(file, audio);

    // inicio de cada palabra
    const startOf = new Map(timepoints.map((tp) => [tp.markName, tp.timeSeconds]));
    let timing = 'marks';
    let starts;
    if (tokens.every((t) => startOf.has(`w${t.i}`))) {
      starts = tokens.map((t) => startOf.get(`w${t.i}`));
    } else {
      // Plan B: reparto proporcional por letras (menos preciso)
      timing = 'fallback-proporcional';
      const lens = tokens.map((t) => t.display.length + 1);
      const sum = lens.reduce((a, b) => a + b, 0);
      let acc = 0;
      starts = lens.map((l) => { const st = (acc / sum) * info.duration; acc += l; return st; });
    }
    const words = tokens.map((t, k) => ({
      text: t.display,
      emphasis: t.emphasis,
      start: +starts[k].toFixed(3),
      end: +((k + 1 < tokens.length ? starts[k + 1] : info.duration)).toFixed(3),
    }));

    out.slides.push({ n: s.n, audio: file.replace(/\\/g, '/'), duration: +info.duration.toFixed(3), timing, words });
    totalSecs += info.duration;
    console.log(`Slide ${s.n}: ${info.duration.toFixed(2)}s · ${tokens.length} palabras · tiempos: ${timing}`);
  }

  await writeFile('build/timings.json', JSON.stringify(out, null, 2));
  console.log(`\nVoz total: ${totalSecs.toFixed(1)}s (el video final suma ~${(totalSecs + cfg.slides.length * 0.55).toFixed(0)}s con pausas).`);
  console.log('Tiempos guardados en build/timings.json');
  if (out.slides.some((s) => s.timing !== 'marks')) {
    console.log('\n⚠ Algún slide usó tiempos proporcionales: esta voz no devolvió marcas. Prueba otra con --probe.');
  }
}

(flag('--deep') ? deep() : flag('--probe') ? probe() : generate()).catch((e) => { console.error('Error:', e.message); process.exit(1); });
