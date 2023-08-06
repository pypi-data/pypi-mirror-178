import datetime

from compute_service.api.crud import Session, get_task
from compute_service.api.models import Status


def start(db: Session, task_uuid: str):
    task = get_task(db, task_uuid)
    task.status = Status.in_progress
    task.started = datetime.datetime.utcnow()
    db.commit()


def success(db: Session, task_uuid: str, result: dict):
    task = get_task(db, task_uuid)
    task.status = Status.success
    task.finished = datetime.datetime.utcnow()
    task.result = result
    db.commit()


def error(db: Session, task_uuid: str, error_msg: str):
    task = get_task(db, task_uuid)
    task.status = Status.error
    task.finished = datetime.datetime.utcnow()
    task.error_msg = error_msg
    db.commit()


def details(db: Session, task_uuid: str, details: dict):
    task = get_task(db, task_uuid)
    task.details = details
    db.commit()
