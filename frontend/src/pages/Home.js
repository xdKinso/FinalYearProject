import React, { useState, useEffect } from 'react';
import api from '../components/api'; // Import your custom Axios instance
import "./App.css";

const Home = () => {
    const [currentTime, setCurrentTime] = useState(0);
    const [userName, setUserName] = useState('');

    useEffect(() => {
        // Fetch current time
        api.get('/time')
            .then(response => {
                setCurrentTime(response.data.time);
            })
            .catch(error => {
                console.error("There was an error fetching the current time:", error);
            });

        // Fetch user details
        api.get('/profile')
            .then(response => {
                if (response.data && response.data.Username) {
                    setUserName(response.data.Username);
                }
            })
            .catch(error => {
                // Handle error or redirect to login if unauthorized
                console.error("There was an error fetching user data:", error);
            });
    }, []);

    return (
        <div>
            <header className="App-header">
                {userName && <h2>Hello, {userName}!</h2>}
                <p>Welcome to Krystian's Stat Tracker</p>
                <p>The current time is {currentTime}.</p>
                <h1>Welcome to the Home page!</h1>
                <p>This is a simple React component for the Home page.</p>
            </header>
        </div>
    );
};

export default Home;
