from datetime import datetime
from typing import Union

from pydantic import BaseModel

from compute_service.api.models import Status
from compute_service.api.config import APIConfig


class TaskCreate(BaseModel):
    input_params: APIConfig().input_model

class TaskUpdate(BaseModel):
    started: Union[datetime, None] = None
    finished: Union[datetime, None] = None
    status: Union[Status, None] = None
    error_msg: Union[str, None] = None
    result: Union[dict, None] = None
    details: Union[dict, None] = None

class Task(TaskCreate, TaskUpdate):
    uuid: str
    created: datetime

    class Config:
        orm_mode = True
