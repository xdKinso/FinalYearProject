import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, BrowserRouter, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./App.css";
import Home from "./pages/Home.js";
import About from "./pages/About.js";
import Navbar from "./Navigation/Navbar.js";
import Login from "./pages/Login.js";
import Register from "./pages/Register.js";
import Profile from './pages/Profile.js';
import Update from './pages/Update.js'
import FortniteStats from './pages/Fnstats.js';

function App() {
  return (
    <div className="App">
        <Navbar/>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/Login" element={<Login/>} />
            <Route path="/register" element={<Register/>} />
            <Route path="/Profile" element = {<Profile/>}/>
            <Route path="/Profile/Update" element = {<Update/>}/>
            <Route path="/Fnstats" element={<FortniteStats />} />
          </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
