import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

function UpdateProfile() {
    const [dateOfBirth, setDateOfBirth] = useState('');
    const [bio, setBio] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Implement what happens when the form is submitted
        console.log({ dateOfBirth, bio });
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formDateOfBirth">
                <Form.Label>Date of Birth</Form.Label>
                <Form.Control
                    type="date"
                    value={dateOfBirth}
                    onChange={(e) => setDateOfBirth(e.target.value)}
                />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBio">
                <Form.Label>Bio (Max 250 Characters)</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    maxLength={250}
                />
                <Form.Text className="text-muted">
                    {bio.length}/250 characters
                </Form.Text>
            </Form.Group>

            <Button variant="primary" type="submit">
                Confirm Changes
            </Button>
        </Form>
    );
}

export default UpdateProfile;
