import React, { useState } from "react";

const EmailSender = () => {
  const [subject, setSubject] = useState("Hey {{name}}, exciting opportunity!");
  const [body, setBody] = useState(
    `Hi {{name}},\n\nI'm reaching out with a cool opportunity I think you'll love!\n\nCheers,\nYour Name`
  );
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const API_BASE = process.env.REACT_APP_BACKEND_URL.replace(/\/+$/, ""); // remove trailing slash

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

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>Mass Email Sender</h2>

      <label>Subject:</label>
      <input
        type="text"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />

      <label>Body:</label>
      <textarea
        rows="10"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />

      <button onClick={sendEmails} disabled={loading}>
        {loading ? "Sending..." : "Send Emails"}
      </button>

      {status && <p style={{ marginTop: 10 }}>{status}</p>}
    </div>
  );
};

export default EmailSender;
