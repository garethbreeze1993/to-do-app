import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card"
import Pagination from "react-bootstrap/Pagination";
import React from "react"
import { useLocation } from "react-router-dom"
import CardGroup from "react-bootstrap/CardGroup";
import Alert from "react-bootstrap/Alert";
import Button from "react-bootstrap/Button";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import base_api from "../base_api";
import {changeDateLayout, checkDeadlinePassed, sadfrownImg, notCompletedIcon, completedIcon} from "../helpers";


export default function Home(props) {
    const [taskObj, setTaskObj] = React.useState([]);
    const [allTaskObj, setAllTaskObj] = React.useState([]);
    const [totalEntries, setTotalEntries] = React.useState(0)
    const [page, setPage] = React.useState(1);
    const size = 10;
    const locState  = useLocation();
    const deletePage = locState.state ? locState.state.deleteObj : false;
    const [reportGenerated, setReportGenerated] = React.useState(false);

    // url = {{URL}}tasks?page=1&size=25
    // Get total and size from API request to determine how many pages needed
    // Hardcode for now to implement frontend

    React.useEffect(() => {
        base_api.get(`/api/v1/tasks/?page=${page}&size=${size}`)
            .then(function (response) {
                setTaskObj(response.data.items)
                setTotalEntries(response.data.total)
            })
            .catch(function (error) {
                if (error.response.data.detail === 'Could not validate credentials'){
                }
            })
    }, [page])

    function calculateNoOfPages(totalEntries, size){
       let pages = totalEntries / size
       if(pages < 1){
           return 1
       }
       else if(! Number.isInteger(pages)){
           return Math.ceil(pages)
       }else{
           return pages
       }
    }

    const numberOfPages = calculateNoOfPages(totalEntries, size)

    React.useEffect(() => {
        base_api.get(`/api/v1/tasks/`)
            .then(function (response){
                setAllTaskObj(response.data.items)
            })
            .catch((error) => {
                console.error(error);
        })
    }, [])

    let items = [];
    for (let number = 1; number <= numberOfPages; number++) {
      items.push(
        <Pagination.Item key={number} active={number === page} onClick={() => setPage(number)}>
          {number}
        </Pagination.Item>,
      );
    }

    const tasks = taskObj.map((task) => {
        return <CardGroup key={task.id}>
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
                    <Card.Link href={`/tasks/${task.id}`}>More Details</Card.Link>
                  </Card.Body>
            </Card>
                </CardGroup>
    })

    const handleReportClick = () => {
        base_api.get('/api/v1/reports/')
            .then(data => {
                setReportGenerated(true)})
            .catch(error => {
                console.log(error)
            })
    }

    const returnContent = totalEntries > 0 ?
        <>
            <div className={"row justify-content-between"} style={{marginTop: "25px"}}>
                <div className={"col-4"}>
                    <h1>Tasks</h1>
                </div>
                <div className={"col-4"}>
                    <Button variant={"primary"} onClick={handleReportClick}>Generate Report for User</Button>
                </div>
            </div>
            {tasks}
            <p>You have {totalEntries} tasks in total of which {allTaskObj.filter((task_) => task_.completed === true).length} are completed</p>
            <Pagination>{items}</Pagination>
            </>
        :
        <>
            <h4>No Tasks created yet</h4>
            {!props.loggedIn && <h5>Please Login to view tasks</h5>}
        </>
    return (
        <section>
            <Container>
                {deletePage && <Alert variant={"success"}>{"Task successfully deleted!"}</Alert>}
                {reportGenerated && <Alert variant={"success"}>
                    Report Generated. Please check your email to download the report</Alert>}
                {returnContent}
            </Container>
        </section>
    )
}
