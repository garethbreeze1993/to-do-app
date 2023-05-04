from pathlib import Path

from background_tasks.app_tasks import create_task_report_for_user
from tests.database import MockDBSession


def test_create_task_report_for_user(mocker, test_user, create_test_tasks):
    file_name = f'test_{test_user["email"]}'
    csv_path = f"/home/gareth/Documents/Projects/to-do-app/backend/local_storage/{file_name}"
    expected_csv_data = [["Task 1", "31/08/2022", "True", "N/A"], ["Task 2", "N/A", "False", "N/A"],
                         ["Task 3",	"31/08/2022", "False", "YES"]]
    patch_1 = mocker.patch("background_tasks.celery_database.celery_db_session.query",
                           return_value=MockDBSession(return_val=create_test_tasks, owner_id=test_user['id'],
                                                      owner_filter=True))
    patch_2 = mocker.patch('background_tasks.app_tasks.return_path_to_csv_file_and_filename',
                           return_value=(csv_path, file_name))
    patch_3 = mocker.patch('background_tasks.app_tasks.get_data_for_csv_file', return_value=(expected_csv_data, 1, 1))
    patch_4 = mocker.patch('background_tasks.app_tasks.make_csv_file')
    patch_5 = mocker.patch('background_tasks.app_tasks.gmail.send')
    create_task_report_for_user(test_user['id'], test_user['email'])
    patch_2.assert_called_with(user_email=test_user['email'])
    patch_3.assert_called_with(tasks=patch_1.return_value)
    patch_4.assert_called_with(csv_path=csv_path, task_data=expected_csv_data, task_count=patch_1.return_value.count(),
                               task_completed=1, task_deadline_passed=1)
    patch_5.assert_called_with(subject='Your generated report', receivers=[test_user['email']],
                               text='Please find attached to this email your task report.',
                               attachments={file_name: Path(csv_path)})
