import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import api from '../components/api'; // Import your Axios instance

function BasicForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');

    try {
      const response = await api.post('/register', { username, email, password });

      if (response.status === 200) {
        setSuccessMessage('User successfully registered!'); // Set success message
        setTimeout(() => {
          window.location.href = '/login'; // Redirect to home
        }, 2000);
      } else {
        setErrorMessage('Registration failed'); // Set error message
      }
    } catch (error) {
      console.error('An error occurred:', error);
      setErrorMessage(error.response?.data?.msg || 'An error occurred. Please try again later.'); // Set error message for network errors
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formBasicUsername">
        <Form.Label>Username</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </Form.Group>

      {successMessage && <div className="alert alert-success" role="alert">{successMessage}</div>}
      {errorMessage && <div className="alert alert-danger" role="alert">{errorMessage}</div>}

      <Button variant="primary" type="submit">Submit</Button>
    </Form>
  );
}

export default BasicForm;
