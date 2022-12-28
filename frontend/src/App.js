import './App.css';
import Home from "./components/Home";
import NavComponent from "./components/Navbar"
import React from "react";
import base_api from "./base_api";

function App() {
    const [loggedIn, setLoggedIn] = React.useState(false);
    const [userEmail, setUserEmail] = React.useState('');
    const userToken = localStorage.getItem('userToken');

    React.useEffect(() => {
    if(userToken){
    base_api.get(`/api/v1/users/get_user_data`)
        .then((response) => {
            setLoggedIn(true)
            setUserEmail(response.data.email)
          })
        .catch(err => {
          setLoggedIn(false)
        })
    }
  }, [userToken])

    return (
    <>
        <NavComponent
            userEmail={userEmail}
            loggedIn={loggedIn}
        />
      <Home />
    </>
  );
}

export default App;
