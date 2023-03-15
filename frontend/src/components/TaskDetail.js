import NavComponent from "./Navbar"
import HTTP404 from "./HTTP404";
import { useParams } from "react-router-dom";
import React from "react";
import { useNavigate } from "react-router-dom";
import Alert from 'react-bootstrap/Alert';
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import CardGroup from "react-bootstrap/CardGroup";
import Container from "react-bootstrap/Container";
import base_api from "../base_api";
import {changeDateLayout, checkDeadlinePassed, sadfrownImg, completedIcon, notCompletedIcon} from "../helpers";


function TaskDetail() {
    let params = useParams();
    let navigate = useNavigate();
    const [task, setTask] = React.useState({});
    const [error, setError] = React.useState(false);
    const [banner, setBanner] = React.useState(false);
    const [bannerMsg, setBannerMsg] = React.useState(false);
    const [bannerLvl, setBannerLvl] = React.useState('');
    const [loggedIn, setLoggedIn] = React.useState(false);
    const [userEmail, setUserEmail] = React.useState('');

    const userToken = localStorage.getItem('userToken');

    React.useEffect(() => {
        base_api.get(`/api/v1/users/get_user_data`)
            .then((response) => {
                setLoggedIn(true)
                setUserEmail(response.data.email)
              })
            .catch(err => {
              setLoggedIn(false)
            })
      }, [userToken])

    let taskId = parseInt(params.taskID, 10) || false;

    React.useEffect(() => {
        base_api.get(`/api/v1/tasks/${taskId}`)
            .then(function (response) {
                setTask(response.data)
            })
            .catch(function (error) {
                if(error.response.status === 404 || error.response.status === 401){
                    setTask(false);
                }else {
                    setError(true)
                }
            })
    }, [taskId])

    function handleComplete () {
        base_api.put(`/api/v1/tasks/complete/${taskId}`, {"completed": true})
            .then(function (response) {
                setTask(response.data);
                setBanner(true);
                setBannerMsg('Task is now complete')
                setBannerLvl("success")
            })
            .catch(function (error) {
                setBanner(true);
                setBannerMsg('Unable to complete contact the system administrator')
                setBannerLvl("danger")
            })
    }

    function handleDelete () {
        base_api.delete(`/api/v1/tasks/${taskId}`)
            .then(function (response) {
                navigate("/", { state: { deleteObj: true } });
            })
            .catch(function (error) {
                console.error(error)
                setBanner(true);
                setBannerMsg('Unable to delete contact the system administrator')
                setBannerLvl("danger")
        })
    }


    const taskFound = task ?
                    <>
                    <CardGroup key={task.id}>
                <Card>
                      <Card.Body>
                        <Card.Title>{task.title}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">{task.deadline && changeDateLayout(task.deadline)}</Card.Subtitle>
                          {task.deadline && <Card.Text>{checkDeadlinePassed(task) && sadfrownImg}</Card.Text>}
                        <Card.Text>
                            {task.description}
                        </Card.Text>
                          <Card.Text>
                              {"Completed - "}{task.completed ? completedIcon : notCompletedIcon}
                        </Card.Text>
                      </Card.Body>
                </Card>
                    </CardGroup>
                    <Button variant="danger" onClick={handleDelete}>Delete</Button> {!task.completed
                    && <Button variant="success" onClick={handleComplete}>Complete Task</Button>}
                    </>
                    : <HTTP404 />

    return (
        <main>
            <NavComponent
                userEmail={userEmail}
                loggedIn={loggedIn}
            />
            <Container>
                {banner && <Alert variant={bannerLvl}>{bannerMsg}</Alert>}
                {!error && taskFound}
                {error && <h4>Error when connecting to server please try again later!</h4>}
            </Container>
        </main>
   );
}

export default TaskDetail;