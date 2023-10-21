// NavigationBar.js
import React from "react";
//import { BrowserRouter as Router, Route, Link } from "react-router-dom";
//import Home from "./Home";
import { Link } from "react-router-dom";
import About from "./About";
import Play from "./Play";
//import NavigationBar from "./NavigationBar";

function NavigationBar() {
  const navStyle = {
    width: '100%',
    background: '#e9f4fb',
    padding: "10px",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)", // Box shadow for a subtle elevation
  };

  const ulStyle = {
    listStyle: "none",
    display: "flex",
    justifyContent: "center",
    gap: "200px",
    padding: "0", // Remove default padding
  };

  const linkStyle = {
    textDecoration: "none",
    color: "#555", // Default text color
    transition: "color 0.3s", // Smooth color transition on hover
    fontWeight: "bold", // Make text bold
    fontSize: "22px", // Increase font size
    cursor: "pointer", // Change cursor to a pointer on hover
  };

  // Style for text on hover
  const linkHoverStyle = {
    color: "Red", // Text color on hover
  };

  return (
    <nav style={navStyle}>
      <ul style={ulStyle}>
        <li><a href="/" style={linkStyle}>Home</a></li>
        <li><a href="/about" style={linkStyle}>About</a></li>
        <li><a href="/play" style={linkStyle}>Play</a></li>
      </ul>
    </nav>
  );
}

export default NavigationBar;
