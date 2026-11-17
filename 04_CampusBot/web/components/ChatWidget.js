"use client";

import { useEffect, useRef, useState } from "react";

const GREETING = "Bonjour ! Je suis CampusBot 🎓 Posez-moi vos questions sur l'École Schulz.";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]); // tout l'historique, gardé dans le navigateur
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);
  const inputRef = useRef(null);

  // Défile vers le bas à chaque nouveau morceau de réponse.
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight });
  }, [messages]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  // Met à jour le dernier message (la réponse en cours).
  const updateLast = (patch) =>
    setMessages((prev) => {
      const copy = [...prev];
      copy[copy.length - 1] = { ...copy[copy.length - 1], ...patch };
      return copy;
    });

  async function send(e) {
    e?.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    // On renvoie tout l'historique (sans les messages d'erreur) + la nouvelle question.
    const history = [
      ...messages.filter((m) => !m.error),
      { role: "user", content: text },
    ].map(({ role, content }) => ({ role, content }));

    setMessages([...messages, { role: "user", content: text }, { role: "assistant", content: "" }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });

      if (!res.ok || !res.body) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Erreur du serveur.");
      }

      // Lecture du flux : on ajoute chaque morceau au fur et à mesure.
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let answer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        answer += decoder.decode(value, { stream: true });
        updateLast({ content: answer });
      }
      if (!answer.trim()) updateLast({ content: "(pas de réponse)", error: true });
    } catch (err) {
      updateLast({ content: `⚠️ ${err.message}`, error: true });
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  return (
    <>
      {open && (
        <section className="cb-panel" role="dialog" aria-label="CampusBot">
          <header className="cb-header">
            <div>
              <strong>CampusBot</strong>
              <span>Assistant de l'École Schulz</span>
            </div>
            <button className="cb-close" onClick={() => setOpen(false)} aria-label="Fermer">
              ×
            </button>
          </header>

          <div className="cb-messages" ref={listRef} aria-live="polite">
            <div className="cb-msg cb-assistant">{GREETING}</div>
            {messages.map((m, i) => (
              <div key={i} className={`cb-msg cb-${m.role}${m.error ? " cb-error" : ""}`}>
                {m.content || <span className="cb-typing"><i /><i /><i /></span>}
              </div>
            ))}
          </div>

          <form className="cb-form" onSubmit={send}>
            <input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Posez votre question…"
              maxLength={2000}
              aria-label="Votre message"
            />
            <button type="submit" disabled={loading || !input.trim()} aria-label="Envoyer">
              ➤
            </button>
          </form>
        </section>
      )}

      <button
        className="cb-bubble"
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? "Fermer CampusBot" : "Ouvrir CampusBot"}
      >
        {open ? "×" : "💬"}
      </button>
    </>
  );
}
