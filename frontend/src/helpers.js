import React from "react";

export function checkDeadlinePassed(task){
    let deadlineDate = new Date(task.deadline);
    deadlineDate.setHours(23, 59, 59)
    let todaysDate = new Date();

    if(!task.completed){
        if (todaysDate > deadlineDate){
            return true
        }
    }
    return false
}

export function changeDateLayout(deadline){
    const deadline_arr = deadline.split('-')
    return `${deadline_arr[2]}/${deadline_arr[1]}/${deadline_arr[0]}`
}

export const completedIcon = <i className="bi bi-check-circle-fill" style={{"fontSize": "2rem", "color": "green"}}></i>
export const notCompletedIcon = <i className="bi bi-x-circle-fill" style={{"fontSize": "2rem", "color": "red"}}></i>
export const sadfrownImg = <>{"Deadline Passed - "}<i className="bi bi-emoji-frown" style={{"fontSize": "2rem"}}></i></>