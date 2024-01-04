import React, { useState, useEffect } from 'react';
import "./App.css";
const Home = () => {
    const [currentTime, setCurrentTime] = React.useState(0);
    useEffect(() => {
        fetch('/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time);
        });
      }, []);

  return (
    <div>
        <header className="App-header">
          Welcome to Krystian's Stat Tracker
          <p>The current time is {currentTime}.</p>

          <h1>Welcome to the Home page!</h1>
          <p>This is a simple React component for the Home page.</p>
        </header>
    </div>
  );
};

export default Home;
