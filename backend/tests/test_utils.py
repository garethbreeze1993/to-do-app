import csv
from datetime import datetime
import os

from app.config import settings
from app.utils import return_path_to_csv_file_and_filename, make_csv_file, get_data_for_csv_file
from tests.database import MockDBSession


def test_return_path_to_csv_file_and_filename(test_user):

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
    csv_filename = f'report_{test_user["email"]}_{timestamp}.csv'

    expected_csv_path, expected_filename = return_path_to_csv_file_and_filename(test_user['email'])

    # Get the directory the file will live in remove filename
    split_up_path = expected_csv_path.split('/')[:-1]
    expected_file_directory = '/'.join(split_up_path)
    assert expected_file_directory == local_file_storage_path

    # test filename made correctly
    assert expected_filename.endswith('.csv')
    expected_filename_split = expected_filename.split('_')
    actual_filename_split = csv_filename.split('_')
    assert expected_filename_split[0] == actual_filename_split[0]
    assert expected_filename_split[1] == actual_filename_split[1]
    expected_datestring = expected_filename_split[2][:-4]
    actual_datestring = actual_filename_split[2][:-4]
    expected_date_from_name = datetime.strptime(expected_datestring, '%Y-%m-%d-%H-%M-%S').date()
    actual_date_from_name = datetime.strptime(actual_datestring, '%Y-%m-%d-%H-%M-%S').date()
    assert expected_date_from_name == actual_date_from_name


def test_get_data_for_csv_file(create_test_tasks, test_user):
    create_test_tasks_filtered = [task for task in create_test_tasks if task.owner_id == test_user['id']]

    expected_task_data = []
    expected_task_deadline_passed = 0

    for task in create_test_tasks_filtered:
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
            expected_task_deadline_passed += 1

        expected_task_data.append(task_row)

    actual_task_data, actual_task_completed, actual_task_deadline_passed = get_data_for_csv_file(
        tasks=MockDBSession(return_val=create_test_tasks_filtered, completed_check=True))

    assert expected_task_data == actual_task_data
    assert actual_task_completed == 1
    assert expected_task_deadline_passed == actual_task_deadline_passed


def test_make_csv_file():
    test_data = [['Task 1', '31/08/2022', 'True', 'N/A'], ['Task 2', 'N/A', 'False', 'N/A'],
                 ['Task 3', '31/08/2022', 'False', 'YES']]
    task_complete = 1
    task_deadline_pass = 1
    csv_path = '/home/gareth/Documents/Projects/to-do-app/backend/local_storage/' \
               'report_gareth.breeze@garethbreezecode.com_test.csv'
    make_csv_file(csv_path=csv_path, task_data=test_data, task_count=len(test_data), task_completed=task_complete,
                  task_deadline_passed=task_deadline_pass)

    fields = ['title', 'deadline', 'task_completed', 'task_deadline_passed']

    with open(csv_path, 'r') as test_csv_file:
        csv_reader = csv.reader(test_csv_file, dialect='excel')
        for index, row in enumerate(csv_reader):
            if index == 0:
                assert row == fields
            elif 1 <= index <= 3:
                assert row == test_data[index - 1]
            elif index == 4:
                assert row == ["Total Tasks", f"{len(test_data)}", "", ""]
            elif index == 5:
                assert row == ["Tasks Completed", f"{task_complete}", "", ""]
            elif index == 6:
                assert row == ["Tasks Deadline Passed", f"{task_deadline_pass}", "", ""]

    os.remove(csv_path)
