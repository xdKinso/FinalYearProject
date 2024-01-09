import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import api from '../components/api'; // Import your Axios instance
//basic form 
//setting variables
function BasicForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (event) => {
    //setting default messages
    event.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');
    //trying to use the api
    try {
      const response = await api.post('/login', { email, password });
      //when you log in you will get redirected to home page
      if (response.status === 200) {
        const data = response.data;
        console.log(data); // Log success (for debugging)
        setSuccessMessage("Login successful! You will be redirected shortly...");
        sessionStorage.setItem('token', data.access_token);
        setTimeout(() => {
          window.location.href = '/'; // Redirect to home after 2 seconds
        }, 2000);
      } else {
        setErrorMessage('Login failed'); 
      }
    } catch (error) {
      console.error('An error occurred:', error);
      //if i get null as a error message or response fall back to default value
      //example: if a username or email is the same it will tell the user
      setErrorMessage(error.response?.data?.msg || "An error occurred. Please try again later.");
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
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

      {/* Success Message Display */}
      {successMessage && (
        <div className="alert alert-success" role="alert">
          {successMessage}
        </div>
      )}

      {/* Error Message Display */}
      {errorMessage && (
        <div className="alert alert-danger" role="alert">
          {errorMessage}
        </div>
      )}

      <Button variant="primary" type="submit">
        Submit
      </Button>
      <Button href="/Register" variant="secondary">Register</Button>
    </Form>
  );
}

export default BasicForm;
