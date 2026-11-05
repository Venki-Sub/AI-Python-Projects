// Limite simple en mémoire : N requêtes par minute et par adresse IP.
// Suffisant pour un seul serveur. Avec plusieurs serveurs, il faudrait
// un stockage partagé (Redis, etc.).

const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = Number(process.env.RATE_LIMIT_PER_MIN) || 10;

const hits = new Map(); // ip -> [timestamps]

export function rateLimit(key) {
  const now = Date.now();
  const recent = (hits.get(key) || []).filter((t) => now - t < WINDOW_MS);

  if (recent.length >= MAX_PER_WINDOW) {
    hits.set(key, recent);
    const retryAfter = Math.ceil((WINDOW_MS - (now - recent[0])) / 1000);
    return { ok: false, retryAfter };
  }

  recent.push(now);
  hits.set(key, recent);

  // Ménage occasionnel pour que la Map ne grossisse pas indéfiniment.
  if (hits.size > 5000) {
    for (const [k, times] of hits) {
      if (times.every((t) => now - t >= WINDOW_MS)) hits.delete(k);
    }
  }

  return { ok: true };
}
