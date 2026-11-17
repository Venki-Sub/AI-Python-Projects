// POST /api/chat  —  reçoit { messages } et renvoie la réponse en streaming (texte brut).
// Ce fichier tourne UNIQUEMENT côté serveur : la clé API n'est jamais envoyée au navigateur.

import Anthropic from "@anthropic-ai/sdk";
import { rateLimit } from "../../../lib/rateLimit";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SYSTEM =
  "Tu es CampusBot, assistant de l'École Schulz. Réponds en français, court et clair. Si tu ne sais pas, dis-le.";

// "ollama" (par défaut, local) ou "anthropic"
const PROVIDER = (process.env.PROVIDER || "ollama").toLowerCase();

const OLLAMA_URL = process.env.OLLAMA_URL || "http://localhost:11434";
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || "llama3.2:3b";

const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || "claude-opus-5-5";
// Modèles qui acceptent le repli automatique côté serveur en cas de refus.
const FALLBACK_MODELS = new Set(["claude-opus-5-5", "claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5"]);

const MAX_MESSAGES = 30; // on ne garde que les 30 derniers messages
const MAX_CHARS = 2000; // longueur max d'un message
const MAX_BODY = 100_000; // taille max de la requête (octets)

// --- Validation : on n'accepte que des messages user/assistant en texte. ---
// Un message "system" envoyé par le navigateur est ignoré : seul le serveur fixe le prompt système.
function cleanMessages(messages) {
  if (!Array.isArray(messages)) return null;

  const out = messages
    .filter(
      (m) =>
        m &&
        (m.role === "user" || m.role === "assistant") &&
        typeof m.content === "string" &&
        m.content.trim() !== ""
    )
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }))
    .slice(-MAX_MESSAGES);

  while (out.length && out[0].role !== "user") out.shift(); // doit commencer par l'utilisateur
  if (!out.length || out[out.length - 1].role !== "user") return null; // doit finir par une question
  return out;
}

// --- Fournisseur 1 : Ollama (local) ---
async function* streamOllama(messages, signal) {
  const res = await fetch(`${OLLAMA_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: OLLAMA_MODEL,
      stream: true,
      messages: [{ role: "system", content: SYSTEM }, ...messages],
    }),
    signal,
  });
  if (!res.ok || !res.body) throw new Error(`Ollama HTTP ${res.status}`);

  // Ollama renvoie une ligne JSON par morceau de texte.
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  const parse = (line) => {
    const data = JSON.parse(line);
    if (data.error) throw new Error(data.error);
    return data.message?.content || "";
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let nl;
    while ((nl = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, nl).trim();
      buffer = buffer.slice(nl + 1);
      if (line) {
        const text = parse(line);
        if (text) yield text;
      }
    }
  }
  if (buffer.trim()) {
    const text = parse(buffer.trim());
    if (text) yield text;
  }
}

// --- Fournisseur 2 : API Anthropic (clé dans process.env.API_KEY) ---
let anthropic;
function getAnthropic() {
  if (!process.env.API_KEY) throw new Error("API_KEY manquante dans .env.local");
  anthropic ??= new Anthropic({ apiKey: process.env.API_KEY });
  return anthropic;
}

async function* streamAnthropic(messages, signal) {
  const params = {
    model: ANTHROPIC_MODEL,
    max_tokens: 1024, // réponses courtes : plafond de coût
    system: SYSTEM,
    messages,
    output_config: { effort: "low" }, // un chatbot FAQ n'a pas besoin de réfléchir longtemps
  };
  if (FALLBACK_MODELS.has(ANTHROPIC_MODEL)) {
    params.betas = ["server-side-fallback-2026-07-01"];
    params.fallbacks = "default";
  }

  const stream = getAnthropic().beta.messages.stream(params, { signal });
  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      yield event.delta.text;
    }
  }
  const final = await stream.finalMessage();
  if (final.stop_reason === "refusal") yield "\n\nJe ne peux pas répondre à cette demande.";
}

// --- La route ---
export async function POST(req) {
  const ip =
    req.headers.get("x-forwarded-for")?.split(",")[0].trim() ||
    req.headers.get("x-real-ip") ||
    "local";

  const limit = rateLimit(ip);
  if (!limit.ok) {
    return Response.json(
      { error: `Trop de messages. Réessayez dans ${limit.retryAfter} s.` },
      { status: 429, headers: { "Retry-After": String(limit.retryAfter) } }
    );
  }

  let body;
  try {
    const raw = await req.text();
    if (raw.length > MAX_BODY) return Response.json({ error: "Requête trop longue." }, { status: 413 });
    body = JSON.parse(raw);
  } catch {
    return Response.json({ error: "JSON invalide." }, { status: 400 });
  }

  const messages = cleanMessages(body?.messages);
  if (!messages) return Response.json({ error: "Format de messages invalide." }, { status: 400 });

  const generate = PROVIDER === "anthropic" ? streamAnthropic : streamOllama;
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      try {
        for await (const chunk of generate(messages, req.signal)) {
          controller.enqueue(encoder.encode(chunk));
        }
      } catch (err) {
        if (!req.signal.aborted) {
          console.error("[/api/chat]", err); // détail dans le terminal du serveur, pas dans le navigateur
          controller.enqueue(encoder.encode("\n\n⚠️ CampusBot est indisponible pour le moment."));
        }
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      "X-Accel-Buffering": "no",
    },
  });
}
