// retry.mjs — reintento con backoff exponencial para llamadas a APIs externas (Drive, Google Cloud TTS).
//
// Por que existe (29-oct-2026): con el fix de concurrency por pieza, las 7 piezas de un lote
// pueden correr en paralelo ahora. A ese volumen la CUOTA de las APIs no es el riesgo real
// (Neural2 TTS permite 1000 solicitudes/minuto por proyecto; 7 piezas * ~6 slides = ~42
// llamadas, muy por debajo). El riesgo real es un error TRANSITORIO de red (timeout, 429,
// 500-504) en cualquier llamada individual -- hoy eso hace fallar el run COMPLETO (30 min de
// render perdidos) por un fallo de 1-2 segundos que un segundo intento resolveria solo.
//
// Mismo patron que ya usa drive_client.py (_open(), retries=4, sleep 2**i) del lado Python --
// este modulo es el equivalente para el lado Node (tts.mjs, fetch_assets.mjs), que llamaban a
// sus APIs sin ningun retry propio.
//
// Uso:
//   import { withRetry } from '../_ci/retry.mjs';
//   const res = await withRetry(() => client.synthesizeSpeech({...}));

const RETRYABLE_HTTP = new Set([429, 500, 502, 503, 504]);

function isRetryable(err) {
  // Codigo HTTP explicito (fetch/google-auth-library suelen exponerlo en err.code o err.status)
  const code = err?.code ?? err?.status ?? err?.response?.status;
  if (RETRYABLE_HTTP.has(code)) return true;
  // google-cloud/text-to-speech (gRPC) usa err.code numerico de gRPC: 8=RESOURCE_EXHAUSTED
  // (cuota/rate-limit), 14=UNAVAILABLE (transitorio de servidor), 4=DEADLINE_EXCEEDED (timeout)
  if (code === 8 || code === 14 || code === 4) return true;
  // Errores de red de bajo nivel (timeout, conexion reiniciada, DNS transitorio)
  const netCodes = new Set(['ETIMEDOUT', 'ECONNRESET', 'ECONNREFUSED', 'EAI_AGAIN', 'ENOTFOUND']);
  if (netCodes.has(err?.code)) return true;
  return false;
}

/**
 * Ejecuta `fn` y reintenta ante errores transitorios (429/5xx/timeouts de red), con backoff
 * exponencial (1s, 2s, 4s, ... hasta `retries` intentos en total). Relanza el error tal cual
 * si no es retryable, o si se agotaron los intentos -- nunca oculta un fallo real (ej. texto
 * invalido, credenciales faltantes).
 */
export async function withRetry(fn, { retries = 4, label = 'llamada' } = {}) {
  let lastErr;
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (!isRetryable(err) || i === retries - 1) throw err;
      const wait = 2 ** i * 1000;
      console.warn(`! ${label}: error transitorio (${err.code ?? err.message}), reintento ${i + 1}/${retries - 1} en ${wait / 1000}s...`);
      await new Promise((r) => setTimeout(r, wait));
    }
  }
  throw lastErr; // inalcanzable, satisface a linters estrictos
}
