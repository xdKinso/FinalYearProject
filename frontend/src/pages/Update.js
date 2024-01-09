import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import api from "../components/api.js"; 
//update profile page
function UpdateProfile() {
    const [DOB, setDateOfBirth] = useState('');
    const [Bio, setBio] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        setErrorMessage('');
        setSuccessMessage('');

        // Basic validation 
        if (!DOB || !Bio) {
            setErrorMessage("Please fill in all fields.");
            return;
        }

        try {
            const response = await api.post("/profile/update", { DOB, Bio });

            if (response.status === 200) {
                console.log(response.data); // Log success
                setSuccessMessage("Profile successfully updated!");
                setTimeout(() => {
                    window.location.href = '/profile'; // Redirect to profile page
                }, 2000);
            } else {
                setErrorMessage('Update failed');
            }
        } catch (error) {
            console.error('An error occurred:', error);
            setErrorMessage(error.response?.data?.msg || "An error occurred. Please try again later.");
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formDateOfBirth">
                <Form.Label>Date of Birth</Form.Label>
                <Form.Control
                    type="date"
                    value={DOB}
                    onChange={(e) => setDateOfBirth(e.target.value)}
                />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBio">
                <Form.Label>Bio (Max 250 Characters)</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    value={Bio}
                    onChange={(e) => setBio(e.target.value)}
                    maxLength={250}
                />
                <Form.Text className="text-muted">
                    {Bio.length}/250 characters
                </Form.Text>
            </Form.Group>

            {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
            {successMessage && <div className="alert alert-success">{successMessage}</div>}

            <Button variant="primary" type="submit">
                Confirm Changes
            </Button>
        </Form>
    );
}

export default UpdateProfile;
