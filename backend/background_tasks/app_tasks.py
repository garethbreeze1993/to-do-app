from celery.utils.log import get_task_logger

from .celery import celery_app
from app import models
from background_tasks.celery_database import SqlAlchemyTask, celery_db_session

log = get_task_logger(__name__)


@celery_app.task(base=SqlAlchemyTask)
def create_task_report_for_user(owner_id: int):
    """
    Celery Task to generate a report of all the tasks that are associated by the user
    ::param owner_id: The models.User.id
    ::return None
    """
    tasks = celery_db_session.query(models.Task) \
        .filter(models.Task.owner_id == owner_id)

    task_count = tasks.count()

    log.info(f'task count = {task_count}')

    for task in tasks:
        log.info(f"id = {task.id}")
        log.info(f"title = {task.title}")

    return True
