import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../components/api'; // Adjust the import path as necessary
import "./user-profile.css"

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const { userID } = useParams();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get(`/users/${userID}`);
                setUser(response.data);
            } catch (error) {
                console.error('Error fetching user details:', error);
            }
        };

        fetchUser();
    }, [userID]);

    if (!user) {
        return <div><h1>Loading...</h1></div>;
    }

    return (
        <div className="user-profile">
            <h1>User Profile</h1>
            <div className="profile-card">
                <h2>{user.Username}</h2>
                <p>{user.Bio}</p>
                <p>{user.Age}</p>
            </div>
        </div>
    );
};

export default UserProfile;
