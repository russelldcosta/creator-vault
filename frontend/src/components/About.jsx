import React from "react";
import Navbar from "./Navbar";
import "./HomePage.css";

const About = () => {
  return (
    <div className="homepage">
      <Navbar />

      <section className="how-section" style={{ marginTop: "80px" }}>
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: "40px",
            textAlign: "left",
          }}
        >
          <div style={{ flex: "1 1 500px" }}>
            <h2 className="section-title" style={{ textAlign: "left" }}>Hi, I’m Russell D'Costa</h2>
            <p className="section-text">
                I'm a 4th year Computer Science student interested in developing solutions to time consuming problems.
            </p>
            <p className="section-text">
                The inspiration for this site came from a year ago when I wanted to reach out to streamers to try out my game, as a solo developer up against
                AAA game publishers, your only valuable resource is time, you're least likely to expend capital on marketing your game considering the high stakes involved.
                Which leaves you your only option of cold mailing streamers to try out your game, which is a very time consuming process from first hand experience.
                This solution tackles that problem by spreading the word of your game to those willing streamers interested in that genre.
            </p>
            <p className="section-text">
            Mass-Emailing web apps already exist and Websites offering streamers paid databases exist aswell, 
            but no web app exists which offers both features for free under one umbrella where it automates marketing for solo dev while saving them much needed time.
            </p>
          </div>

          <img
            src="/images/my-photo.jpeg"
            alt="Profile"
            style={{
              width: "400px",
              borderRadius: "12px",
              objectFit: "cover",
              flexShrink: 0,
            }}
          />
        </div>
      </section>
    </div>
  );
};

export default About;
