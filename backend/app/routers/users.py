import logging

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app import oauth2
from app.schemas import UserCreate, UserResponse
from app.utils import get_password_hash

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


# @router.get('/foo')
# def foo():
#     log.info('using tasks router')
#     return {"Hello": "Worldxmxm"}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db_session: Session = Depends(get_db)):

    new_user = models.User()
    new_user.email = user.email
    hashed_password = get_password_hash(password=user.password)
    new_user.password = hashed_password
    db_session.add(new_user)

    try:
        db_session.commit()
    except exc.SQLAlchemyError as e:
        log.error('Problem with sqlalchemy when creating user')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unexpected problem please check the request and try again')

    db_session.refresh(new_user)

    return new_user


@router.get("/get_user_data")
def get_logged_in_user_data(current_user: 'models.User' = Depends(oauth2.get_current_user)):
    return {'email': current_user.email}
