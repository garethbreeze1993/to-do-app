import React from "react"
import Nav from "./Navbar"
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form';
import base_api from "../base_api";

function Create() {
    const [formValues, setFormValues] = React.useState({formTitle: '', formDescription: '', formDeadline: ''})
    const [formSubmitted, setFormsubmitted] = React.useState(false);
    const [formError, setFormError] = React.useState(false);
    const [formErrorMsg, setFormErrorMsg] = React.useState('');

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

    function handleSubmit(event, valueObj){
        event.preventDefault();

        if (valueObj.formTitle === '' || valueObj.formDescription === ''){
            setFormError(true);
            setFormErrorMsg("Missing value(s) when submitting form please fill out both the title and description fields")
            return
        }
        let dataObject = {title: valueObj.formTitle, description: valueObj.formDescription}
        if(valueObj.formDeadline !== ''){
            dataObject['deadline'] = valueObj.formDeadline
        }

        base_api.post(`/tasks/`, dataObject)
            .then(function (response) {
                setFormValues({formTitle: '', formDescription: '', formDeadline: ''})
                setFormsubmitted(true)
                console.log(response);
                })
            .catch(function (error) {
                setFormError(true)
                if (error.response.data.detail === 'Could not validate credentials'){
                    setFormErrorMsg("You need to be logged in to create a post.")
                }
                else{
                    setFormErrorMsg("Error when submitting form. Please try again later.")
                }
                console.log(error);
            });

    }

    return (
      <main>
          <Nav />
          <Container>
              {formSubmitted && <Alert variant={"success"}>Form successfully submitted!</Alert>}
              {formError && <Alert variant={"danger"}>{formErrorMsg}</Alert>}
              <Form onSubmit={(event) => {handleSubmit(event, formValues)}}>
                  <Form.Group className="mb-3" controlId="formTitle">
                      <Form.Label>Title</Form.Label>
                      <Form.Control type="text" placeholder="Enter title" value={formValues['formTitle']} name={"formTitle"}
                                    onChange={handleChange} />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formDescription">
                    <Form.Label>Description</Form.Label>
                    <Form.Control type="textarea" placeholder="Description" value={formValues['formDescription']}
                                  name={"formDescription"} onChange={handleChange} />
                  </Form.Group>
                  <Form.Group className="mb-3" controlId="formDeadline">
                      <Form.Label>Deadline</Form.Label>
                      <Form.Control type="date" placeholder="Deadline" value={formValues['formDeadline']}
                                    name={"formDeadline"} onChange={handleChange} />
                  </Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
          </Container>
      </main>
  );
}

export default Create;