from celery.utils.log import get_task_logger

from .celery import celery_app
from app import models
from app.utils import make_csv_file, return_path_to_csv_file
from background_tasks.celery_database import SqlAlchemyTask, celery_db_session

log = get_task_logger(__name__)


@celery_app.task(base=SqlAlchemyTask)
def create_task_report_for_user(owner_id: int, user_email: str) -> None:
    """
    Celery Task to generate a report of all the tasks that are associated by the user
    ::param owner_id: The models.User.id
    ::param user_email: models.User.email
    ::return None
    """

    tasks = celery_db_session.query(models.Task) \
        .filter(models.Task.owner_id == owner_id)

    task_count = tasks.count()

    csv_path = return_path_to_csv_file(user_email=user_email)

    make_csv_file(csv_path=csv_path, tasks=tasks, task_count=task_count)

    return
