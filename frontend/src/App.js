import './App.css';
import Home from "./components/Home";
import NavComponent from "./components/Navbar"
import React from "react";
import { Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <>
        <NavComponent />
      <Home />
    </>
  );
}

export default App;
