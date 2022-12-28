import React from "react";
import Navbar from 'react-bootstrap/Navbar';
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import 'bootstrap/dist/css/bootstrap.min.css';
import base_api from "../base_api";


function NavComponent(props) {

  return (
    <>
        <Navbar bg="dark" variant="dark">
            <Container>
            <Navbar.Brand href="/">Todoo App</Navbar.Brand>
            <Nav className="me-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>
              {props.loggedIn && <Nav.Link href="/create">Create</Nav.Link>}
            </Nav>
              <Navbar.Collapse className="justify-content-end">
                {!props.loggedIn ?
                    <>
                      <Nav.Link href="/login">Log in</Nav.Link>
                      <Nav.Link href="/signup">Sign Up</Nav.Link>
                    </>
                    :
                    <>
                      <Navbar.Text>
                        Signed in as: {props.userEmail}
                      </Navbar.Text>
                      <Nav.Link href="/logout">Log Out</Nav.Link>
                    </>
                }
              </Navbar.Collapse>
            </Container>
        </Navbar>
    </>
  );
}

export default NavComponent;