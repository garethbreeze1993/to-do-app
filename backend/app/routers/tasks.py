import logging

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi_pagination import paginate, Page
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app import oauth2
from app.schemas import TaskResponse, TaskCreate, TaskComplete

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("/", response_model=Page[TaskResponse])
def get_tasks_for_user(db_session: Session = Depends(get_db),
                       current_user: 'models.User' = Depends(oauth2.get_current_user)):
    owner_id = current_user.id
    tasks = db_session.query(models.Task)\
        .filter(models.Task.owner_id == owner_id)\
        .all()
    return paginate(tasks)


@router.get("/{id_}", response_model=TaskResponse)
def get_task(id_: int, db_session: Session = Depends(get_db),
             current_user: 'models.User' = Depends(oauth2.get_current_user)):
    owner_id = current_user.id

    task = db_session.query(models.Task)\
        .filter(models.Task.id == id_,
                models.Task.owner_id == owner_id)\
        .first()

    if not task:
        log.error(f'Task not found with id={id_} get task detail get request')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task not found with id={id_}')

    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate, db_session: Session = Depends(get_db),
                current_user: 'models.User' = Depends(oauth2.get_current_user)):
    task_dict = task_input.dict()
    task = models.Task(**task_dict)
    task.owner_id = current_user.id

    db_session.add(task)

    try:
        db_session.commit()
    except exc.SQLAlchemyError as e:
        log.error('Error creating task sql alchemy')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unexpected problem please check the request and try again')

    db_session.refresh(task)

    return task


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id_: int, db_session: Session = Depends(get_db),
                current_user: 'models.User' = Depends(oauth2.get_current_user)):
    task = db_session.query(models.Task).get(id_)
    owner_id = current_user.id

    if not task:
        log.error(f'Task not found id={id_} when deleting task')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task not found id={id_}')

    if task.owner_id != owner_id:
        log.error(f'Not authorised to perform requested action wrong user trying to delete other user post')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')

    db_session.delete(task)

    try:
        db_session.commit()
    except exc.SQLAlchemyError as e:
        log.error('Error sqlalchemy when trying to delete post')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unexpected problem please check the request and try again')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_}", response_model=TaskResponse)
def update_task(id_: int, task_input: TaskCreate, db_session: Session = Depends(get_db),
                current_user: 'models.User' = Depends(oauth2.get_current_user)):
    task = db_session.query(models.Task).get(id_)
    owner_id = current_user.id

    if not task:
        log.error(f'Task not found id={id_} update task')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task not found id={id_}')

    if task.owner_id != owner_id:
        log.error('Not authorised to update task wrong user')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')

    for field in ['title', 'description', 'deadline']:
        setattr(task, field, getattr(task_input, field))

    db_session.add(task)

    try:
        db_session.commit()
    except exc.SQLAlchemyError as e:
        log.error('Error for update method when updating task')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unexpected problem please check the request and try again')

    db_session.refresh(task)

    return task


@router.put("/complete/{id_}", response_model=TaskResponse)
def complete_task(id_: int, task_input: TaskComplete, db_session: Session = Depends(get_db),
                  current_user: 'models.User' = Depends(oauth2.get_current_user)):
    task = db_session.query(models.Task).get(id_)
    owner_id = current_user.id

    if not task:
        log.error(f'Task not found id={id_} complete task')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task not found id={id_}')

    if task.owner_id != owner_id:
        log.error(f'Not authorised to complete task wrong user')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')

    task.completed = task_input.completed

    db_session.add(task)

    try:
        db_session.commit()
    except exc.SQLAlchemyError as e:
        log.error('Problem with sqlalchemy complete task')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unexpected problem please check the request and try again')

    db_session.refresh(task)

    return task
