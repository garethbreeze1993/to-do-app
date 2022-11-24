import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import './index.css';
import App from './App';
import About from "./components/About";
import Create from "./components/Create";
import HTTP404 from "./components/HTTP404";
import Login from "./components/Login";
import LogOut from "./components/LogOut";
import TaskDetail from "./components/TaskDetail";
import SignUp from "./components/SignUp";

import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<App />} />
              <Route path="/about" element={<About />} />
              <Route path="/create" element={<Create />} />
              <Route path="tasks/:taskID" element={<TaskDetail />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/logout" element={<LogOut />} />
              <Route path="*" element={<HTTP404 />} />
            </Routes>
      </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
