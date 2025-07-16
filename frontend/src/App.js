// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import CategoryEmailPage from "./components/CategoryEmailPage";
import About from "./components/About";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/get-started" element={<CategoryEmailPage />} />
        <Route path="/about" element={<About/>} />
      </Routes>
    </Router>
  );
}

export default App;



// npm install react-scripts
// npm install