from celery import Celery
from background_tasks import celeryconfig


celery_app = Celery(__name__)

celery_app.config_from_object(celeryconfig)


if __name__ == '__main__':
    celery_app.start()
