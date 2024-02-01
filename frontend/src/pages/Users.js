import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../components/api'; // Import the Axios instance
import './users.css';

const UserTable = () => {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await api.get('/users');
                setUsers(response.data);
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        };

        fetchUsers();
    }, []);

    const handleUserClick = userID => {
        navigate(`/users/${userID}`);
    };

    return (
        <div className="user-container">
            {users.map(user => (
                <div key={String(user.User_ID)} className="user-box" onClick={() => handleUserClick(user.User_ID)}>
                    <p><strong>ID:</strong> {user.User_ID}</p>
                    <p><strong>Username:</strong> {user.Username}</p>
                </div>
            ))}
        </div>
    );
};

export default UserTable;
