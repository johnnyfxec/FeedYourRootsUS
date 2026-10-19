// lib.mjs — utilidades compartidas por tts.mjs y render.mjs (PZA_5.3)

export const BRAND = {
  white: '#FFFFFF',
  gold: '#E8B84B',
  brown: '#5C3A1E',
  parchment: '#F5ECD7',
};

// ---------- Guion -> tokens ----------
// Marcas del guion: *palabra* = énfasis (se quita antes del TTS).
export const PAUSE = { sentence: 380, colon: 200, comma: 100, ellipsis: 500, extra: 450 };
export function tokenize(text) {
  return text.trim().split(/\s+/).map((raw, i) => {
    let t = raw;
    let emphasis = false;
    if (t.includes('*')) { emphasis = true; t = t.replace(/\*/g, ''); }
    let pause = 0;
    let extra = 0;
    if (/\/\/$/.test(t)) { extra = PAUSE.extra; t = t.replace(/\/\/$/, ''); }
    if (/(…|\.\.\.)$/.test(t)) { pause = PAUSE.ellipsis; t = t.replace(/(…|\.\.\.)$/, ','); }
    else if (/[.?!]$/.test(t)) pause = PAUSE.sentence;
    else if (/:$/.test(t)) pause = PAUSE.colon;
    else if (/,$/.test(t)) pause = PAUSE.comma;
    const display = t.replace(/[.,:;]+$/, '');
    pause += extra;
    return { i, speak: t, display, emphasis, pause };
  });
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function toSSML(tokens) {
  const body = tokens
    .map((t) => `<mark name="w${t.i}"/>${esc(t.speak)}${t.pause ? `<break time="${t.pause}ms"/>` : ''}`)
    .join(' ');
  return `<speak>${body}</speak>`;
}

// ---------- WAV ----------
export function wavInfo(buf) {
  const ch = buf.readUInt16LE(22);
  const sr = buf.readUInt32LE(24);
  const bits = buf.readUInt16LE(34);
  let off = 12;
  while (off < buf.length - 8) {
    const id = buf.toString('ascii', off, off + 4);
    const size = buf.readUInt32LE(off + 4);
    if (id === 'data') {
      const bytes = Math.min(size, buf.length - off - 8);
      return { sr, ch, bits, duration: bytes / (sr * ch * (bits / 8)) };
    }
    off += 8 + size;
  }
  throw new Error('WAV sin chunk data');
}

// ---------- Variantes ----------
// Id de variante:  A  |  B  con modificadores:  -e14 (énfasis 1.4x)  -nm (sin movimiento)  -up (MAYÚSCULAS)
// Ejemplos: "A", "B-e14", "B-e18-up", "B-e10-nm"
export function parseVariant(id) {
  const [style, ...mods] = id.split('-');
  const v = { id, style, emphasis: 1.4, motion: true, upper: false, gold: false, outline: false, dim: false };
  if (!['A', 'B'].includes(style)) throw new Error(`Variante desconocida: ${id}`);
  for (const m of mods) {
    if (/^e\d+$/.test(m)) v.emphasis = parseInt(m.slice(1), 10) / 10;
    else if (m === 'nm') v.motion = false;
    else if (m === 'up') v.upper = true;
    else if (m === 'gold') v.gold = true;
    else if (m === 'so') v.outline = true;
    else if (m === 'dim') v.dim = true;
    else throw new Error(`Modificador desconocido "${m}" en ${id}`);
  }
  return v;
}

// ---------- Source de Clipkit ----------
const HEAD = 0.15;   // silencio antes de la voz en cada slide
const TAIL = 0.65;   // silencio después de la voz
const TAIL_LAST = parseFloat(process.env.FYR_TAIL_LAST || '0.35');  // cierre B: 0.35; cierre A: FYR_TAIL_LAST=0.05 (espera del loop recortada a la mitad, 10-oct)
const XFADE = 0.25;  // crossfade entre slides

export function buildSource({ cfg, timings, variant, base, fontOk }) {
  const v = parseVariant(variant);
  const W = cfg.canvas.w, H = cfg.canvas.h;
  const elements = [];
  const fonts = [];
  const fam = cfg.fuente_subtitulos;
  if (fontOk && fam) fonts.push({ family: fam.family, weight: fam.weight, src: `${base}/${fam.file}` });
  const fontFamily = (fontOk && fam ? fam.family : 'Inter') + ', sans-serif';

  // línea de tiempo
  let t = 0;
  const slides = cfg.slides.map((s, idx) => {
    const tm = timings.slides.find((x) => x.n === s.n);
    if (!tm) throw new Error(`Falta timing del slide ${s.n}. Corre tts.mjs primero.`);
    const last = idx === cfg.slides.length - 1;
    const dur = HEAD + tm.duration + (last ? TAIL_LAST : TAIL);
    const row = { ...s, tm, start: t, dur, last, voiceAt: t + HEAD };
    t += dur;
    return row;
  });
  const total = +t.toFixed(3);

  // imágenes
  slides.forEach((s, idx) => {
    const el = {
      id: `img${s.n}`,
      type: 'image',
      layer: 1 + idx,
      source: `${base}/${s.imagen}`,
      x: 0, y: 0, width: W, height: H,
      fit: 'cover',
      time: +s.start.toFixed(3),
      duration: +(s.dur + (s.last ? 0 : XFADE)).toFixed(3),
    };
    if (idx > 0) el.animations = [{ type: 'fade-in', duration: XFADE, easing: 'ease-out' }];
    if (v.dim && idx > 0) el.brightness = 0.82;
    if (v.motion && s.movimiento !== false) {
      el.keyframe_animations = [{
        property: 'scale',
        easing: 'linear',
        keyframes: [{ time: 0, value: 1.0 }, { time: +s.dur.toFixed(3), value: 1.07 }],
      }];
    }
    elements.push(el);
  });

  // audio
  slides.forEach((s, idx) => {
    elements.push({
      id: `voz${s.n}`,
      type: 'audio',
      layer: 50 + idx,
      source: `${base}/${s.tm.audio}`,
      time: +s.voiceAt.toFixed(3),
      duration: +s.tm.duration.toFixed(3),
      volume: 100,
    });
  });

  // subtítulos (solo slides con subtitulos != false)
  const words = [];
  for (const s of slides) {
    if (s.subtitulos === false) continue;
    for (const w of s.tm.words) {
      words.push({
        text: v.upper ? w.text.toUpperCase() : w.text,
        emphasis: w.emphasis,
        start: +(s.voiceAt + w.start).toFixed(3),
        end: +(s.voiceAt + w.end).toFixed(3),
      });
    }
  }

  const BASE_SIZE = 104;
  const common = {
    x: '50%', x_anchor: '50%', y: '52%', y_anchor: '50%',
    text_align: 'center',
    font_family: fontFamily,
    font_weight: fam ? fam.weight : '700',
    ...(v.outline ? { stroke_color: BRAND.brown, stroke_width: 12 } : {}),
    text_shadow: [
      { color: '#000000', offset_x: 0, offset_y: 4, blur: 4, opacity: 0.55 },
      { color: '#000000', offset_x: 0, offset_y: 8, blur: 22, opacity: 0.55 },
    ],
  };

  if (v.style === 'A') {
    // Caption nativo de Clipkit: palabra activa resaltada en dorado, sin énfasis de tamaño.
    elements.push({
      ...common,
      id: 'subs',
      type: 'caption',
      layer: 100,
      time: 0,
      duration: 'end',
      width: 940,
      height: 520,
      words: words.map((w) => ({ text: w.text, start: w.start, end: w.end })),
      style: 'tiktok_bounce',
      max_length: 16,
      font_size: BASE_SIZE,
      fill_color: BRAND.white,
      highlight_color: BRAND.gold,
    });
  } else {
    // B: una palabra a la vez, cada una su propio elemento; énfasis = más grande y dorado.
    words.forEach((w, k) => {
      elements.push({
        ...common,
        id: `w${k}`,
        type: 'text',
        layer: 100 + k,
        time: w.start,
        duration: +Math.max(0.12, w.end - w.start).toFixed(3),
        width: 960,
        text: w.text,
        font_size: Math.min(Math.round(BASE_SIZE * (w.emphasis ? v.emphasis : 1)), Math.floor(900 / (Math.max(1, w.text.length) * (v.upper ? 0.66 : 0.58)))),
        fill_color: w.emphasis && v.gold ? BRAND.gold : BRAND.white,
        // (los presets de animación no corren con stroke; se usan keyframes)
        keyframe_animations: [{
          property: 'scale',
          keyframes: [{ time: 0, value: 0.78 }, { time: 0.14, value: 1, easing: 'ease-out-back' }],
        }],
      });
    });
  }

  return {
    clipkit_version: '1.0',
    output_format: 'mp4',
    width: W,
    height: H,
    duration: total,
    frame_rate: 30,
    background_color: BRAND.parchment,
    ...(fonts.length ? { fonts } : {}),
    elements,
  };
}
