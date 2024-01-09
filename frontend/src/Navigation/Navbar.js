import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
//my navbar i am using bootstrap to help add a little bit of style
function BasicExample() {
  const token = sessionStorage.getItem('token'); // Using sessionStorage

  const handleLogout = () => {
    sessionStorage.removeItem('token'); // Removing token from sessionStorage
    window.location.href = '/'; // Redirect to home after logout
  };

  return (
    <Navbar bg="dark" data-bs-theme="dark" expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/">KST</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/Fnstats">Fnstats</Nav.Link>
            <Nav.Link href="/About">About</Nav.Link>
            
            {/* Show 'Profile' if logged in, otherwise show 'Login' */}
            {token ? (
              <Nav.Link href="/Profile">Profile</Nav.Link>
            ) : (
              <Nav.Link href="/Login">Login</Nav.Link>
            )}

            <NavDropdown title="Dropdown" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          {token && (
            <Button
              onClick={handleLogout}
              style={{ backgroundColor: 'red', borderColor: 'red' }}
            >
              Logout
            </Button>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default BasicExample;
