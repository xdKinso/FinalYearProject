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
//for some reason some imports are red when they are correct (they work so its not an issue i think i havent turned off visual studio in a while and renamed files )
function App() {
  //im only using this for routing right now i think i can implement certain stuff here like the use token but im not surei have used the(api component so maybe ill keep it the way it is)
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
