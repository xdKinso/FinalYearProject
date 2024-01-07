import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './styles.css'; 

function Profile() {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Initialize useNavigate

    useEffect(() => {
        const fetchData = async () => {
            const token = sessionStorage.getItem('token'); // Get token from sessionStorage
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

            try {
                const response = await fetch('/profile', { headers });
                if (response.ok) {
                    const data = await response.json();
                    setUserData(data);
                } else {
                    setError('Failed to fetch profile data.');
                }
            } catch (err) {
                setError('An error occurred.');
            }
        };

        fetchData();
    }, []);

    const handleUpdateClick = () => {
        navigate('/profile/update'); // Navigate to /profile/update on button click
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!userData) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Profile</h1>
            <p><strong>Username:</strong> {userData.Username}</p>
            <p><strong>Email:</strong> {userData.Email}</p>
            <p><strong>Bio:</strong> {userData.Bio}</p>
            <p><strong>Date Of Birth: </strong>{userData.Age}</p>
            <div className='top-right'>
                <Button variant="primary" onClick={handleUpdateClick}>Update Profile</Button>
            </div>
        </div>
    );
}

export default Profile;
