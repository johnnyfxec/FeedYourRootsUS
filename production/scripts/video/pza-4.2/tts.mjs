// tts.mjs — genera la voz (un WAV por slide) + tiempos de cada palabra, para PZA_4.2
//
//   node tts.mjs --probe            -> prueba varias voces: ¿devuelven marcas de palabra? + WAV de muestra para escucharlas
//   node tts.mjs                    -> genera audio de todos los slides con la voz de pieza_4.2.json
//   node tts.mjs --voice en-US-Neural2-H   -> igual pero con otra voz
//
// Requiere: GOOGLE_APPLICATION_CREDENTIALS apuntando al JSON de credenciales.

import textToSpeech from '@google-cloud/text-to-speech';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { tokenize, toSSML, wavInfo } from './lib.mjs';

const client = new textToSpeech.v1beta1.TextToSpeechClient();
const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };

async function synth({ ssml, name, languageCode = 'en-US', speakingRate = 1.0 }) {
  const [res] = await client.synthesizeSpeech({
    input: { ssml },
    voice: { languageCode, name },
    audioConfig: { audioEncoding: 'LINEAR16', sampleRateHertz: 24000, speakingRate },
    enableTimePointing: ['SSML_MARK'],
  });
  return { audio: Buffer.from(res.audioContent), timepoints: res.timepoints || [] };
}

async function probe() {
  const voices = [
    'en-US-Neural2-C', 'en-US-Neural2-F', 'en-US-Neural2-H', 'en-US-Neural2-J',
    'en-US-Wavenet-F', 'en-US-Wavenet-H',
    'en-US-Studio-O', 'en-US-Studio-Q',
    'en-US-Standard-F',
    'en-US-Journey-F',
  ];
  const text = "Number *five*: fill the seed tray. Soil doesn't care how small the hands are.";
  const tokens = tokenize(text);
  const ssml = toSSML(tokens);
  await mkdir('build/probe', { recursive: true });
  console.log(`Palabras en el texto de prueba: ${tokens.length}\n`);
  console.log('VOZ                      MARCAS  DURACIÓN  ESTADO');
  for (const name of voices) {
    try {
      const { audio, timepoints } = await synth({ ssml, name });
      const d = wavInfo(audio).duration;
      await writeFile(`build/probe/${name}.wav`, audio);
      const ok = timepoints.length === tokens.length;
      console.log(`${name.padEnd(24)} ${String(timepoints.length).padStart(3)}/${tokens.length}   ${d.toFixed(2).padStart(5)}s   ${ok ? 'OK — sirve para subtítulos palabra por palabra' : 'SIN marcas completas'}`);
    } catch (e) {
      console.log(`${name.padEnd(24)}   —        —      ERROR: ${String(e.message).split('\n')[0].slice(0, 90)}`);
    }
  }
  console.log('\nWAV de muestra en build/probe/ — escúchalos y elige la voz (solo vale una con "OK").');
}

async function generate() {
  const cfg = JSON.parse(await readFile('pieza_4.2.json', 'utf-8'));
  const voice = { ...cfg.voz, ...(opt('--voice') ? { name: opt('--voice') } : {}) };
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

(flag('--probe') ? probe() : generate()).catch((e) => { console.error('Error:', e.message); process.exit(1); });
