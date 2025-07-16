//`Hey {{name}}!,\n\nI'm -Your Name- I hope you're doing fine, I found your channel through itch.io, I make horror games, I understand your time is valuable so you could decide if you want to play my game or not by checking out the videos attached below \n\nCheers,\n-Your Name-`
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const EmailSender = () => {
  const [subject, setSubject] = useState("Hey {{name}}, exciting opportunity!");
  const [body, setBody] = useState(
    `Hey {{name}}!,\n\nI'm -Your Name-, hope you're doing fine, I found your channel through itch.io, I understand your time is valuable so you could decide if you want to play my game or not by checking out the videos attached below \n\nCheers,\n-Your Name-`
  );
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [enhancedText, setEnhancedText] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [selectedText, setSelectedText] = useState("");

  const navigate = useNavigate();
  const API_BASE = process.env.REACT_APP_BACKEND_URL.replace(/\/+$/, "");

  const sendEmails = async () => {
    setLoading(true);
    setStatus("");
    try {
      const response = await fetch(`${API_BASE}/send-emails`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, body }),
      });

      if (response.ok) {
        setStatus("✅ Emails sent successfully!");
      } else {
        const errorData = await response.json();
        setStatus(`❌ Error: ${errorData.detail || "Unknown error"}`);
      }
    } catch (err) {
      setStatus("❌ Network error");
    }
    setLoading(false);
  };

  const captureSelection = () => {
    setTimeout(() => {
      const textarea = document.getElementById("body-textarea");
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selected = textarea.value.substring(start, end).trim();
      setSelectedText(selected);
    }, 50);
  };

  const handleEnhance = async () => {
    if (!selectedText) {
      alert("Please select some text to enhance.");
      return;
    }

    setAiLoading(true);
    setEnhancedText("");

    try {
      const response = await fetch(`${API_BASE}/enhance-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_text: selectedText }),
      });

      const data = await response.json();
      setEnhancedText(data.enhanced_text);
    } catch (err) {
      setEnhancedText("❌ AI failed to enhance the text.");
    }

    setAiLoading(false);
  };

  const copyToClipboard = () => {
    const textarea = document.createElement("textarea");
    textarea.value = enhancedText;
    textarea.style.position = "fixed";  // prevent scroll jump
    textarea.style.opacity = 0;
    textarea.style.pointerEvents = "none";
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
      const successful = document.execCommand("copy");
      if (successful) {
        alert("Copied to clipboard!");
      } else {
        alert("Copy failed. Please try manually.");
      }
    } catch (err) {
      alert("Copy failed. Please try manually.");
    }
    document.body.removeChild(textarea);
  };


  return (
    <div style={styles.wrapper}>
      <label style={styles.label}>Subject</label>
      <input
        type="text"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        style={styles.input}
      />

      <label style={styles.label}>Body</label>
      <textarea
        id="body-textarea"
        rows="10"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        onMouseUp={captureSelection}
        onTouchEnd={captureSelection}
        style={{ ...styles.textarea, userSelect: "text" }}
      />

      <div style={styles.buttonRow}>
        <button
          onClick={() => navigate("/")}
          style={{ ...styles.button, backgroundColor: "#999" }}
        >
          ← Back
        </button>
        <button
          onClick={sendEmails}
          disabled={loading}
          style={styles.button}
        >
          {loading ? "Sending..." : "Send Emails"}
        </button>
        <button
          onClick={handleEnhance}
          style={{ ...styles.button, backgroundColor: "#28a745" }}
        >
          {aiLoading ? "Enhancing..." : "✨ Enhance with AI"}
        </button>
      </div>

      {enhancedText && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <label style={styles.label}>Enhanced Version</label>
          <textarea
            rows="6"
            value={enhancedText}
            readOnly
            style={{ ...styles.textarea, backgroundColor: "#eef" }}
          />
          <button
            onClick={copyToClipboard}
            style={{ ...styles.button, marginTop: "10px" }}
          >
            📋 Copy
          </button>
        </div>
      )}

      {status && <p style={styles.status}>{status}</p>}
    </div>
  );
};

const styles = {
  wrapper: {
    maxWidth: 640,
    margin: "60px auto",
    padding: "30px",
    backgroundColor: "#f9f9f9",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
    fontFamily: "'Helvetica Neue', sans-serif",
    color: "#333",
  },
  label: {
    display: "block",
    fontSize: "14px",
    marginBottom: "6px",
    marginTop: "16px",
  },
  input: {
    width: "100%",
    padding: "10px 12px",
    fontSize: "14px",
    border: "1px solid #ccc",
    borderRadius: "6px",
    outline: "none",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    padding: "12px",
    fontSize: "14px",
    border: "1px solid #ccc",
    borderRadius: "6px",
    outline: "none",
    boxSizing: "border-box",
  },
  buttonRow: {
    marginTop: "24px",
    display: "flex",
    flexWrap: "wrap",
    gap: "12px",
  },
  button: {
    padding: "10px 20px",
    backgroundColor: "#4A90E2",
    color: "#fff",
    fontSize: "14px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    transition: "background 0.2s ease",
  },
  status: {
    marginTop: "16px",
    fontSize: "14px",
  },
};

export default EmailSender;
