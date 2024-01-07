import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function BasicForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState(''); // State for error message
  const [successMessage, setSuccessMessage] = useState(''); // State for success message


  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevents the default form submission behavior
    setErrorMessage(""); // Clear any previous error messages
    setSuccessMessage(""); // Clear any previous success messages

    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }), // Send email and password as JSON
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data); // Log success (for debugging)
        setSuccessMessage("Login successful!"); // Set success message
        sessionStorage.setItem('token', data.access_token);
        setTimeout(() =>{
            window.location.href=('/'); // Redirect to /home
        }, 2000);
        
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.msg || 'Login failed'); // Set specific error message from server
      }
    } catch (error) {
      console.error('An error occurred:', error); // Handle network errors
      setErrorMessage("An error occurred. Please try again later.");
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
