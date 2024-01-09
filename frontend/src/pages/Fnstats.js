import React, { useState } from 'react';
import { Button, Form, FormGroup, FormControl, Alert } from 'react-bootstrap';
import api from '../components/api';
import './styles.css';

function FortniteStats() {
    const [username, setUsername] = useState('');
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');

    const handleSubmitStats = async (e) => {
        e.preventDefault();
        setError('');
        setStats(null);
        try {
            const response = await api.get(`/Fnstats?username=${username}`);
            if (response.data) {
                setStats(response.data);
            }
        } catch (err) {
            setError('Failed to fetch Fortnite stats. Please ensure the username is correct.');
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!currentMessage.trim()) return;

        const userMessage = { sender: 'User', text: currentMessage };
        setChatMessages([...chatMessages, userMessage]);

        try {
            const response = await api.post('/chatbot', { message: currentMessage });
            const botMessage = { sender: 'Bot', text: response.data.response };
            setChatMessages([...chatMessages, botMessage]);
        } catch (error) {
            console.error('Error:', error);
        }

        setCurrentMessage('');
    };

    return (
        <div className="chat-container">
            <div className="stats-container">
                <Form onSubmit={handleSubmitStats}>
                    <FormGroup className="mb-3">
                        <FormControl
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter Fortnite Username"
                        />
                    </FormGroup>
                    <Button variant="primary" type="submit">Get Stats</Button>
                </Form>
                {error && <Alert variant="danger">{error}</Alert>}
                {stats && (
                    <div>
                        <h3>Stats for {username}</h3>
                        <p>Deaths: {stats.data.stats.all.overall.deaths}</p>
                        <p>K/D Ratio: {stats.data.stats.all.overall.kd}</p>
                        <p>Kills: {stats.data.stats.all.overall.kills}</p>
                        <p>Kills Per Match: {stats.data.stats.all.overall.killsPerMatch}</p>
                        <p>Kills Per Minute: {stats.data.stats.all.overall.killsPerMin}</p>
                        <p>Last Modified: {stats.data.stats.all.overall.lastModified}</p>
                        <p>Matches: {stats.data.stats.all.overall.matches}</p>
                        <p>Minutes Played: {stats.data.stats.all.overall.minutesPlayed}</p>
                        <p>Players Outlived: {stats.data.stats.all.overall.playersOutlived}</p>
                        <p>Score: {stats.data.stats.all.overall.score}</p>
                        <p>Score Per Match: {stats.data.stats.all.overall.scorePerMatch}</p>
                        <p>Score Per Minute: {stats.data.stats.all.overall.scorePerMin}</p>
                        <p>Top 5 Finishes: {stats.data.stats.all.overall.top5}</p>
                        <p>Top 12 Finishes: {stats.data.stats.all.overall.top12}</p>
                        <p>Win Rate: {stats.data.stats.all.overall.winRate}%</p>
                        <p>Wins: {stats.data.stats.all.overall.wins}</p>
                    </div>
                )}
            </div>

            <div className="chatbox">
                {chatMessages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                <Form onSubmit={handleSendMessage}>
                    <FormGroup className="mb-3">
                        <FormControl
                            type="text"
                            value={currentMessage}
                            onChange={(e) => setCurrentMessage(e.target.value)}
                            placeholder="Ask the bot..."
                        />
                    </FormGroup>
                    <Button variant="outline-secondary" type="submit">Send</Button>
                </Form>
            </div>
        </div>
    );
}

export default FortniteStats;
