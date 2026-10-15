import React, { useState } from "react";
import "./ChatBot.css";

function ChatBot({ role, onClose }) {
  const [messages, setMessages] = useState([
    { sender: "bot", text: `Hello! I'm the ${role} assistant. How can I help you today?` }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    const userMsg = { sender: "user", text: input };
    const botReply = { sender: "bot", text: "I am a placeholder bot. Implement your AI logic here." };
    setMessages(prev => [...prev, userMsg, botReply]);
    setInput("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="chatbot-overlay">
      <div className="chatbot-window">
        <div className="chatbot-header">
          <h3>{role} Assistant</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>
        <div className="chatbot-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`msg ${msg.sender}`}>{msg.text}</div>
          ))}
        </div>
        <div className="chatbot-input">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
