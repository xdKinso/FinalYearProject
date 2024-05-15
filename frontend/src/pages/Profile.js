import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import api from '../components/api'; // Import your Axios instance
import './styles.css'; 
//profile page for react
function Profile() {
    //setting variables
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Initialize useNavigate

    useEffect(() => {
        const fetchData = async () => {
            try {
                //will fetch /profile to get data from backend
                const response = await api.get('/profile');
                if (response.status === 200) {
                    setUserData(response.data);
                } else {
                    setError('Failed to fetch profile data.');
                }
            } catch (err) {
                if (err.response?.status === 401) {
                    // If unauthorized, navigate to login page
                    navigate('/login');
                } else {
                    setError('An error occurred.');
                }
            }
        };

        fetchData();
    }, [navigate]);

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
        //will add more stuff such as their fortnite name and stats will also add css to make look better
        <div>
            <h1>Profile</h1>
            <p><strong>Username:</strong> {userData.Username}</p>
            <p><strong>Email:</strong> {userData.Email}</p>
            <p><strong>Bio:</strong> {userData.Bio}</p>
            <p><strong>Date Of Birth:</strong> {userData.Age}</p>
            <div className='top-right'>
                <Button variant="primary" onClick={handleUpdateClick}>Update Profile</Button>
            </div>
        </div>
    );
}

export default Profile;
