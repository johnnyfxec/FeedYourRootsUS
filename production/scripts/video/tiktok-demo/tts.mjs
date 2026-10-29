// tts.mjs — genera la voz narrada para el video de demo de TikTok (App Review).
//
// Mismo patron que production/scripts/video/pinterest-demo/tts.mjs: un WAV por SEGMENTO
// de un video YA GRABADO (demo_raw.mp4, pantalla silenciosa, 106.1s) que se compone
// encima en post-produccion con ffmpeg. Mismo motor y mismas marcas de guion
// (*enfasis*, //, …) que pza-4.2 y el demo de Pinterest, via lib.mjs compartido (copia
// identica en este directorio).
//
//   node tts.mjs                 -> genera un WAV + timepoints de palabra por segmento
//
// Requiere: GOOGLE_APPLICATION_CREDENTIALS apuntando al JSON de credenciales (secreto
// GOOGLE_CREDENTIALS_JSON ya usado por render-video.yml y pinterest-demo-tts.yml).
//
// Entrada: narration_segments.json (mismo directorio), con la forma:
//   { "segments": [ { "id", "label", "video_start", "video_end", "max_duration",
//                     "texto_narrado", "allow_overflow_into_next"? }, ... ] }
//
// Salida: build/audio/<id>.wav (uno por segmento) + build/timings.json con, por
// segmento: duracion real sintetizada, si cupo en max_duration, y el timing de cada
// palabra (start/end en segundos, relativos al inicio del propio WAV) — igual forma
// que pza-4.2 usa para los subtitulos palabra por palabra.

import textToSpeech from '@google-cloud/text-to-speech';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { tokenize, toSSML, wavInfo } from './lib.mjs';

const client = new textToSpeech.v1beta1.TextToSpeechClient();

// Misma voz de marca que PZA_4.2 y el demo de Pinterest (consistencia de FYR).
const VOICE = { name: 'en-US-Neural2-J', languageCode: 'en-US', speakingRate: 0.92, pitch: -4 };

async function synth({ ssml, name, languageCode, speakingRate, pitch }) {
  const [res] = await client.synthesizeSpeech({
    input: { ssml },
    voice: { languageCode, name },
    audioConfig: { audioEncoding: 'LINEAR16', sampleRateHertz: 24000, speakingRate, ...(pitch ? { pitch } : {}) },
    enableTimePointing: ['SSML_MARK'],
  });
  return { audio: Buffer.from(res.audioContent), timepoints: res.timepoints || [] };
}

async function generate() {
  const cfg = JSON.parse(await readFile('narration_segments.json', 'utf-8'));
  await mkdir('build/audio', { recursive: true });
  const out = { voz: VOICE, segments: [] };

  for (const s of cfg.segments) {
    const tokens = tokenize(s.texto_narrado);
    const ssml = toSSML(tokens);
    const { audio, timepoints } = await synth({ ssml, ...VOICE });
    const info = wavInfo(audio);
    const file = `build/audio/${s.id}.wav`;
    await writeFile(file, audio);

    const startOf = new Map(timepoints.map((tp) => [tp.markName, tp.timeSeconds]));
    let timing = 'marks';
    let starts;
    if (tokens.every((t) => startOf.has(`w${t.i}`))) {
      starts = tokens.map((t) => startOf.get(`w${t.i}`));
    } else {
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

    const window = s.max_duration;
    const fits = info.duration <= window + 0.05;
    out.segments.push({
      id: s.id,
      label: s.label,
      video_start: s.video_start,
      video_end: s.video_end,
      max_duration: window,
      audio: file,
      duration: +info.duration.toFixed(3),
      fits_window: fits,
      allow_overflow_into_next: !!s.allow_overflow_into_next,
      timing,
      words,
    });

    const flag = fits ? 'OK' : (s.allow_overflow_into_next ? 'EXCEDE (permitido, se solapa con el siguiente paso)' : 'EXCEDE VENTANA -- revisar guion');
    console.log(`${s.id}: ${info.duration.toFixed(2)}s / ventana ${window}s · ${tokens.length} palabras · tiempos: ${timing} · ${flag}`);
  }

  await writeFile('build/timings.json', JSON.stringify(out, null, 2));
  console.log('\nTiempos guardados en build/timings.json');
  const overflow = out.segments.filter((s) => !s.fits_window && !s.allow_overflow_into_next);
  if (overflow.length) {
    console.log(`\n⚠ ${overflow.length} segmento(s) exceden su ventana sin permiso de solape: ${overflow.map((s) => s.id).join(', ')}`);
  }
}

generate().catch((e) => { console.error('Error:', e.message); process.exit(1); });
