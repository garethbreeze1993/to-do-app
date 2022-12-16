import Nav from "./Navbar"
import Alert from "react-bootstrap/Alert";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import React from "react";
import {useNavigate} from "react-router-dom";


function Login() {
    const axios = require('axios').default;
    const [formValues, setFormValues] = React.useState({formEmail: '', formPassword1: ''})
    const [formError, setFormError] = React.useState(false);
    const [formErrorMsg, setFormErrorMsg] = React.useState('');
    let navigate = useNavigate();
    // const loggedIn = true;

    function handleSubmit(event, formValues) {
        event.preventDefault();
        const bodyFormData = new FormData();
        bodyFormData.append('username', formValues.formEmail)
        bodyFormData.append('password', formValues.formPassword1)
        axios.post(`/login`, bodyFormData)
            .then(function (response) {
                setFormValues({formEmail: '', formPassword1: ''})
                localStorage.setItem('userToken', response.data.access_token)
                localStorage.setItem('userRefreshToken', response.data.refresh_token)
                navigate("/");
                })
            .catch(function (error) {
                setFormError(true)
                if(error.response.status === 401){
                    setFormErrorMsg('Username or Password is incorrect')
                }
                else{
                    setFormErrorMsg("Error when submitting form. Please try again later.")
                }
            });

    }

    function handleChange(event){
        const {name, value} = event.target
        setFormValues(prevState => {
            return {...prevState,
                    [name]: value}})
        if(formError){
            setFormError(false)
        }
    }

    return (
        <main>
            <Nav />
            <Container>
              <div>
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

                    <Button variant="primary" type="submit">
                      Login
                    </Button>
                  </Form>
              </div>
            </Container>
        </main>
  );
}

export default Login;