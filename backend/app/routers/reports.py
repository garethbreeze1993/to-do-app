import logging
from fastapi import APIRouter, status, Depends, HTTPException, Response

from app import models
from app import oauth2

from background_tasks.app_tasks import create_task_report_for_user

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get('/')
def get_task_report_for_user(current_user: 'models.User' = Depends(oauth2.get_current_user)):
    create_task_report_for_user.delay(current_user.id)
    return "Success"
