// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./HomePage.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-logo"><Link to="/">Creator Vault</Link></div>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><a href="#">Docs</a></li>
        <li><a href="#">GitHub</a></li>
        <li><Link to="/about">About</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
