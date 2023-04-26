from abc import ABC
from contextlib import contextmanager

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# Structure just to keep until successful connect

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
celery_db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class SqlAlchemyTask(Task):

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        celery_db_session.remove()


