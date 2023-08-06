from sqlalchemy.orm import Session

from compute_service.api import models


def get_tasks(db: Session, skip: int = 0, limit: int = 20) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_uuid: str) -> models.Task:
    return db.query(models.Task).get(task_uuid)


def create_task(db: Session, task: dict) -> models.Task:
    db_task = models.Task(status=models.Status.created)
    db_task.input_params = task.input_params.dict()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_uuid: str, task: dict) -> models.Task:
    db_task = get_task(db, task_uuid)
    if db_task is None:
        return None
    if task.status:
        db_task.status = task.status
    if task.started:
        db_task.started = task.started
    if task.finished:
        db_task.finished = task.finished
    if task.error_msg:
        db_task.error_msg = task.error_msg
    if task.result:
        db_task.result = task.result
    if task.details:
        db_task.details = task.details
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_uuid: str) -> bool:
    task = db.query(models.Task).get(task_uuid)
    if task is None:
        return False
    
    db.delete(task)
    db.commit()
    return True
