import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import EmailSender from "./EmailSender";
import "./HomePage.css";
import Navbar from "./Navbar";

const CategoryEmailPage = () => {
  const [category, setCategory] = useState("");
  const navigate = useNavigate();

  return (
    <div className="homepage">
    <Navbar />

      <section className="how-section">
        <h2 className="section-title">My product is best described as...</h2>
        <form>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="category-dropdown"
            required
          >
            <option value="">-- Select a category --</option>
            <option value="2d">2D Platformer</option>
            <option value="horror">Horror</option>
            <option value="strategy">Strategy</option>
            <option value="rpg">RPG</option>
            <option value="narrative">Narrative-Driven</option>
            <option value="casual">Casual / Idle</option>
          </select>
        </form>
      </section>

      {category && (
        <section className="how-section">
          <h2 className="section-title">
            Mass Email Send to: <em>{category}</em> Creators
          </h2>
          <EmailSender selectedCategory={category} />

          {/* Back to Home Button */}
          <div style={{ marginTop: "20px", textAlign: "center" }}>
          </div>
        </section>
      )}
    </div>
  );
};

export default CategoryEmailPage;
