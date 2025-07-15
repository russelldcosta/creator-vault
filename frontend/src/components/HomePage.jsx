import React from "react";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="homepage">
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-logo">Creator Vault</div>
        <ul className="nav-links">
          <li><a href="#">Docs</a></li>
          <li><a href="#">Examples</a></li>
          <li><a href="#">Download</a></li>
          <li><a href="#">GitHub</a></li>
        </ul>
      </nav>

      {/* Hero Section */}


<section className="hero">
  <div className="hero">
    <h1 className="hero-title">Your Curated Repository for Bulk Emails.</h1>
    <p className="hero-subtitle">
      Creator Vault is a free tool built to minimize time spent on cold-mailing for solo developers.
    </p>
    <a href="#" className="hero-button">Get Started</a>
        <img
          className="hero-image"
          src="/images/ipad.jpg"
          alt="Tool preview"
        />
    </div>
      </section>

    {/* How it works Section */}
    <section className="how-section">
    <h2 className="section-title">How does it work?</h2>
    <div className="steps-container">
        <div className="step-card">
        <img src="/images/step-1.png" alt="Upload CSV" className="step-icon" />
        <h3 className="step-title">Step 1</h3>
        <p className="step-description">Upload your curated list of creators via CSV or Excel.</p>
        </div>

        <div className="step-divider" />

        <div className="step-card">
        <img src="/images/step-2.png" alt="Personalize Template" className="step-icon" />
        <h3 className="step-title">Step 2</h3>
        <p className="step-description">Personalize the email with dynamic variables like <code>{`{{name}}`}</code>.</p>
        </div>

        <div className="step-divider" />

        <div className="step-card">
        <img src="/images/send.png" alt="Send Emails" className="step-icon" />
        <h3 className="step-title">Step 3</h3>
        <p className="step-description">Click "Send" to deliver your message to all recipients at once.</p>
        </div>

        <div className="step-divider" />

        <div className="step-card">
        <img src="/images/wait.png" alt="Wait for Replies" className="step-icon" />
        <h3 className="step-title">Step 4</h3>
        <p className="step-description">Sit back and wait for responses to roll in!</p>
        </div>
    </div>
    </section>

    {/* Why CreatorVault Section */}
    <br/><br/><br/>
    <section className="how-section">
    <h2 className="section-title">Why CreatorVault?</h2>
    <p className="section-text">
        CreatorVault simplifies the creator outreach process for solo developers and small teams.
        Providing a refined repository of active creators waiting to try our your product with their audience, it saves hours of repetitive work,
        helping you focus on building — not on cold emailing.
    </p>
    </section>


      {/* Contact Section */}
      <br/><br/><br/>
      <nav className="navbar"></nav>
      <section className="contact-section">
        <h2 className="section-title">Contact Us</h2>
        <p className="section-text">
          Have feedback, questions, or feature requests?<br />
          Drop us an email at <a href="mailto:creatorvault.team@gmail.com">creatorvault.team@gmail.com</a>.<br />
          We’d love to hear from you.
        </p>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>© {new Date().getFullYear()} Creator Vault. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default HomePage;
