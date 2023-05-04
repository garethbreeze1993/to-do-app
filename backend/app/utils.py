import csv
from datetime import datetime
import os
from typing import Tuple, List

from passlib.context import CryptContext
from sqlalchemy.orm.query import Query

from app import models
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def return_path_to_csv_file_and_filename(user_email: str) -> Tuple[str, str]:
    """
    Function which returns a path to a CSV file
    ::param user_email the logged-in users email
    ::return the path to the CSV file and the name of the csvfile to be attached to the email
    """

    path = os.path.join('/', settings.path_backend_dir)
    local_file_storage_path = os.path.join(path, 'local_storage')

    try:
        os.mkdir(local_file_storage_path)
    except FileExistsError:
        pass

    now = datetime.now()

    # Format the date and time as a string
    timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')

    # Use the timestamp as part of the file name
    csv_filename = f'report_{user_email}_{timestamp}.csv'

    csv_path = os.path.join(local_file_storage_path, csv_filename)

    return csv_path, csv_filename


def get_data_for_csv_file(tasks: Query) -> Tuple[List[list], int, int]:
    """
    Function that gets the necessary data to be used in the CSV file to be exported
    ::param tasks: SQLAlchemy query object of all tasks that are made by the logged-in user
    :: return a Tuple containing the task data in a list of lists, te number of tasks completed
        and the number of tasks where the deadline has passed
    """

    task_data = []
    task_deadline_passed = 0

    for task in tasks:
        task_row = [task.title]
        if task.deadline:
            task_row.append(task.deadline.strftime('%d/%m/%Y'))
        else:
            task_row.append('N/A')

        task_row.append(str(task.completed))

        if not task.deadline or task.completed:
            task_row.append('N/A')
        elif task.deadline >= datetime.now().date():
            task_row.append('NO')
        else:
            task_row.append('YES')
            task_deadline_passed += 1

        task_data.append(task_row)

    task_completed = tasks.filter(models.Task.completed == True) \
        .count()

    return task_data, task_completed, task_deadline_passed


def make_csv_file(csv_path: str, task_data: List[list], task_count: int, task_completed: int,
                  task_deadline_passed: int) -> None:
    """
    Function which takes in a path to a CSV file and the SQLAlchemy query data and makes a CSV report
    ::param csv_path: path to the CSV file
    ::param task_data: A list of lists containing data needed for the CSV file of all the users tasks
    ::param task_count: How many tasks that are associated with the user got by the .count() SQLAlchemy method
    ::param task_completed: The number of completed tasks
    ::param task_deadline_passed The number of tasks where the deadline has passed for completing the tasks
    """

    fields = ['title', 'deadline', 'task_completed', 'task_deadline_passed']

    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(fields)
        csvwriter.writerows(task_data)
        csvwriter.writerow(["Total Tasks", task_count, "", ""])
        csvwriter.writerow(["Tasks Completed", f"{task_completed}", "", ""])
        csvwriter.writerow(["Tasks Deadline Passed", f"{task_deadline_passed}", "", ""])
