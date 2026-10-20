import { useEffect, useRef, useState } from "react";
import "./ChatBot.css";

const assistantDetails = {
  "People & HR": { topics: "people policies, benefits, hiring, and workplace support", prompts: ["How do I get started?", "Where can I find a people policy?", "Who can help with benefits?"] },
  Employee: { topics: "workplace tools, everyday processes, and employee support", prompts: ["How do I get started?", "Where can I find a company policy?", "Who can help me with a request?"] },
  Finance: { topics: "expenses, budgets, invoices, and finance processes", prompts: ["How do I submit an expense?", "Where can I find finance guidance?", "Who can help with an invoice?"] },
  Executive: { topics: "leadership priorities, company planning, and business operations", prompts: ["What can you help me with?", "Where can I find planning guidance?", "How do I get started?"] },
};

function makeDemoReply(question, role, topics) {
  const normalized = question.toLowerCase();
  if (/^(hi|hello|hey)\b/.test(normalized)) return `Hi! I’m your ${role} assistant. I can help you explore ${topics}. What would you like to look into?`;
  if (/\b(help|start|do)\b/.test(normalized)) return `I can help you explore ${topics}. Tell me a little more about what you need and I’ll help you work through it.`;
  return `Thanks for sharing that. I can help you think through ${topics}. This demo isn’t connected to your company’s documents yet, so I can’t confirm internal policies or give company-specific answers.`;
}

function ChatBot({ role, tone, onClose }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const inputRef = useRef(null);
  const endRef = useRef(null);
  const replyTimerRef = useRef(null);
  const details = assistantDetails[role] || assistantDetails.Employee;

  useEffect(() => {
    inputRef.current?.focus();
    const onKeyDown = (event) => { if (event.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.clearTimeout(replyTimerRef.current);
    };
  }, [onClose]);

  useEffect(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), [messages, isTyping]);

  const submitMessage = (rawText) => {
    const text = rawText.trim();
    if (!text) return;
    setMessages((current) => [...current, { sender: "user", text }]);
    setInput("");
    setIsTyping(true);
    window.clearTimeout(replyTimerRef.current);
    replyTimerRef.current = window.setTimeout(() => {
      setMessages((current) => [...current, { sender: "assistant", text: makeDemoReply(text, role, details.topics) }]);
      setIsTyping(false);
    }, 650);
  };

  const handleSend = (event) => {
    event.preventDefault();
    submitMessage(input);
  };

  return (
    <div className="chatbot-overlay" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className={`chatbot-window chatbot-tone-${tone}`} role="dialog" aria-modal="true" aria-labelledby="chat-title">
        <header className="chatbot-header">
          <div className="chat-brand"><span className="chat-brand-icon">✦</span><span><strong id="chat-title">{role} assistant</strong><small><i /> Interactive demo · local replies</small></span></div>
          <button className="close-btn" onClick={onClose} aria-label="Close assistant">×</button>
        </header>
        <div className="chatbot-context"><span>✧</span> Chat with the {role} assistant. Try a suggested question or write your own.</div>
        <div className="chatbot-messages" aria-live="polite">
          {messages.length === 0 ? <div className="chat-welcome" key="welcome">
            <div className="welcome-glow"><span>✦</span></div>
            <p className="chat-eyebrow">YOUR {role.toUpperCase()} ASSISTANT</p>
            <h2>What can I help<br />you find today?</h2>
            <p className="chat-welcome-copy">Ask anything about {details.topics}. This interactive demo responds locally while the company chat service is being built.</p>
            <div className="suggestion-list">{details.prompts.map((suggestion, index) => <button key={suggestion} style={{ "--suggestion-index": index }} onClick={() => submitMessage(suggestion)}>{suggestion}<span>↗</span></button>)}</div>
          </div> : <div className="message-list">{messages.map((message, index) => <div key={`${index}-${message.text}`} className={`message-row ${message.sender}`}><span className="message-avatar">{message.sender === "user" ? "Y" : "✦"}</span><div className="message-bubble">{message.text}</div></div>)}{isTyping && <div className="message-row assistant typing-row"><span className="message-avatar">✦</span><div className="typing-indicator" aria-label="Assistant is replying"><i /><i /><i /></div></div>}</div>}
          <div ref={endRef} />
        </div>
        <form className="chatbot-composer" onSubmit={handleSend}>
          <label className="sr-only" htmlFor="chat-input">Message the {role} assistant</label>
          <textarea ref={inputRef} id="chat-input" value={input} onChange={(event) => setInput(event.target.value)} placeholder={`Ask the ${role} assistant…`} rows="1" disabled={isTyping} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); handleSend(event); } }} />
          <div className="composer-bottom"><span>Demo mode · replies are not company-verified</span><button type="submit" className="send-button" disabled={!input.trim() || isTyping} aria-label="Send message">↑</button></div>
        </form>
        <div className="chat-disclaimer">Please avoid entering sensitive personal information.</div>
      </section>
    </div>
  );
}

export default ChatBot;
