from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from compute_service.api import crud, schemas
from compute_service.api.config import APIConfig


router = APIRouter(tags=["tasks"])

task_queue = APIConfig().queue

# /:
#     GET (skip, limit) - список заданий
#     POST - новое задание
# /{id}:
#     GET - получить задание
#     PATCH - записать результат задания
#     DELETE - удалить задание (и остановить вычисления)


def get_session():
    session = APIConfig().sessionmaker()
    try:
        yield session
    finally:
        session.close()


@router.on_event("startup")
async def startup_event():
    await task_queue.prepare()


@router.on_event("shutdown")
async def shutdown_event():
    await task_queue.release()


@router.get("/", response_model=list[schemas.Task])
async def get_tasks(skip: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    return crud.get_tasks(db, skip, limit)


async def submit_task(task):
    await task_queue.submit(schemas.Task.from_orm(task).json())


@router.post("/", response_model=schemas.Task)
async def post_task(task: schemas.TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    validator = APIConfig().input_validator
    if validator is not None:
        try:
            validator(task.dict()['input_params'])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Validation error: {e}",
            )
    try:
        task = crud.create_task(db, task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid params error: {e}",
        )
    
    background_tasks.add_task(submit_task, task)

    return task


@router.get("/{task_uuid}", response_model=schemas.Task)
async def get_task(task_uuid: str, db: Session = Depends(get_session)):
    task = crud.get_task(db, task_uuid)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch("/{task_uuid}", response_model=schemas.Task)
async def patch_task(task_uuid: str, task: schemas.TaskUpdate, db: Session = Depends(get_session)):
    task = crud.update_task(db, task_uuid, task)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete("/{task_uuid}")
async def delete_task(task_uuid: str, db: Session = Depends(get_session)):
    ret = crud.delete_task(db, task_uuid)
    if not ret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
