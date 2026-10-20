import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ChatInterface.css";

function demoReply(text, assistant) {
  if (/^(hi|hello|hey)\b/i.test(text)) return `Hello! I’m your ${assistant.name} assistant. I can help you explore ${assistant.topics}. What would you like to look into?`;
  if (/\b(help|start)\b/i.test(text)) return `I can help you explore ${assistant.topics}. Tell me a little more about what you need and we can work through it together.`;
  return `Thanks for sharing that. I can help you think through ${assistant.topics}. This chat is currently a local demo and isn’t connected to company documents, so I can’t verify internal policies or company-specific answers yet.`;
}

export default function ChatInterface({ assistant }) {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const endRef = useRef(null);
  const inputRef = useRef(null);
  const timerRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
    return () => window.clearTimeout(timerRef.current);
  }, []);
  useEffect(() => endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }), [messages, typing]);

  const send = (value) => {
    const text = value.trim();
    if (!text || typing) return;
    setMessages((current) => [...current, { sender: "user", text }]);
    setInput("");
    setTyping(true);
    window.clearTimeout(timerRef.current);
    timerRef.current = window.setTimeout(() => {
      setMessages((current) => [...current, { sender: "assistant", text: demoReply(text, assistant) }]);
      setTyping(false);
    }, 700);
  };

  return (
    <main className={`chat-page tone-${assistant.tone}`}>
      <div className="chat-ambient ambient-one" /><div className="chat-ambient ambient-two" />
      <header className="chat-topbar">
        <button className="back-dashboard" onClick={() => navigate("/dashboard")}><span aria-hidden="true">←</span> Assistants</button>
        <a className="chat-page-brand" href="/dashboard"><span className="brand-glyph">h</span> Homeegram</a>
        <span className="chat-secure"><i /> Secure workspace</span>
      </header>
      <section className="conversation-panel" aria-label={`${assistant.name} chat`}>
        <header className="conversation-header">
          <div className="assistant-mark" aria-hidden="true">✦</div>
          <div className="assistant-title"><strong>{assistant.name} assistant</strong><span><i /> Ready to chat <em>·</em> Demo</span></div>
          <span className="conversation-badge">ASSISTANT</span>
        </header>
        <div className="conversation-body" aria-live="polite">
          {messages.length === 0 ? <div className="chat-empty-state">
            <div className="orbital-mark"><span>✦</span><i /><b /></div>
            <p className="chat-kicker">YOUR {assistant.name.toUpperCase()} ASSISTANT</p>
            <h1>A little help,<br />right when you need it.</h1>
            <p className="empty-description">Ask about {assistant.topics}. Start with a suggestion or type your own question.</p>
            <div className="chat-suggestions">{assistant.prompts.map((prompt, index) => <button key={prompt} style={{ "--item-index": index }} onClick={() => send(prompt)}>{prompt}<span>↗</span></button>)}</div>
          </div> : <div className="chat-message-list">{messages.map((message, index) => <article key={`${index}-${message.text}`} className={`chat-message ${message.sender}`}>
            {message.sender === "assistant" && <span className="message-mark">✦</span>}
            <p>{message.text}</p>
          </article>)}{typing && <div className="chat-message assistant"><span className="message-mark">✦</span><div className="chat-typing" aria-label="Assistant is responding"><i /><i /><i /></div></div>}<div ref={endRef} /></div>}
        </div>
        <form className="chat-input-wrap" onSubmit={(event) => { event.preventDefault(); send(input); }}>
          <label className="visually-hidden" htmlFor="message-input">Message the {assistant.name} assistant</label>
          <textarea id="message-input" ref={inputRef} rows="1" value={input} onChange={(event) => setInput(event.target.value)} disabled={typing} placeholder={`Message the ${assistant.name} assistant…`} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); send(input); } }} />
          <div className="input-bottom"><span>Local demo · Don’t include sensitive information</span><button type="submit" disabled={!input.trim() || typing} aria-label="Send message">↑</button></div>
        </form>
        <p className="chat-footnote">Replies are generated locally and are not verified against company information.</p>
      </section>
    </main>
  );
}
