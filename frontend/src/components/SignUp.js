import Nav from "./Navbar"
import Alert from "react-bootstrap/Alert";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import React from "react";

function SignUp() {
    const axios = require('axios').default;
    const [formValues, setFormValues] = React.useState({formEmail: '', formPassword1: '', formPassword2: ''})
    const [formSubmitted, setFormsubmitted] = React.useState(false);
    const [formError, setFormError] = React.useState(false);
    const [formErrorMsg, setFormErrorMsg] = React.useState('');

    function handleSubmit(event, formValues) {
        event.preventDefault();
        if(formValues.formPassword1 !== formValues.formPassword2){
            setFormError(true);
            setFormErrorMsg("Passwords need to match")
            return
        }
        let dataObject = {email: formValues.formEmail, password: formValues.formPassword1}

        axios.post(`/api/v1/users/`, dataObject)
            .then(function (response) {
                setFormValues({formEmail: '', formPassword1: '', formPassword2: ''})
                setFormsubmitted(true)
                })
            .catch(function (error) {
                setFormError(true)
                setFormErrorMsg("Error when submitting form. Please try again later.")
            });

    }

    function handleChange(event){
        const {name, value} = event.target
        setFormValues(prevState => {
            return {...prevState,
                    [name]: value}})
        if(formSubmitted){
            setFormsubmitted(false)
        }
        if(formError){
            setFormError(false)
        }
    }
      return (
        <main>
            <Nav />
            <Container>
                      {formSubmitted && <Alert variant={"success"}><a href={"/login"}>Successfully signed up! Please click the link to Log in</a></Alert>}
                      {formError && <Alert variant={"danger"}>{formErrorMsg}</Alert>}
                      <Form onSubmit={(event) => {handleSubmit(event, formValues)}}>
                          <Form.Group className="mb-3" controlId="formEmail">
                              <Form.Label>Email</Form.Label>
                              <Form.Control type="email" placeholder="Enter Email" value={formValues['formEmail']} name={"formEmail"}
                                            onChange={handleChange} />
                          </Form.Group>

                          <Form.Group className="mb-3" controlId="formPassword1">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" value={formValues['formPassword1']}
                                          name={"formPassword1"} onChange={handleChange} />
                          </Form.Group>

                          <Form.Group className="mb-3" controlId="formPassword2">
                            <Form.Label>Confirm Password</Form.Label>
                            <Form.Control type="password" placeholder="Confirm Password" value={formValues['formPassword2']}
                                          name={"formPassword2"} onChange={handleChange} />
                          </Form.Group>

                        <Button variant="primary" type="submit">
                          Sign Up
                        </Button>
                      </Form>
                  </Container>
        </main>
      );
}

export default SignUp;