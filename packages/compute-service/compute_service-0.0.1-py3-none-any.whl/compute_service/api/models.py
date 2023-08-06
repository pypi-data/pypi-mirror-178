import datetime
import enum
import json
import uuid

from sqlalchemy import Column, DateTime, Enum, String, Text
from sqlalchemy.ext.declarative import declarative_base


class Status(str, enum.Enum):
    created = 'created'
    in_progress = 'in_progress'
    error = 'error'
    success = 'success'


Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    uuid = Column('uuid', Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    started = Column(DateTime)
    finished = Column(DateTime)
    status = Column('status', Enum(Status))
    error_msg = Column(String(50))
    _result = Column(Text())
    _details = Column(Text())
    _input_params = Column(Text())

    @property
    def result(self):
        if self._result is None:
            return None
        return json.loads(self._result)

    @result.setter
    def result(self, value):
        if value is None:
            self._result = None
        else:
            self._result = json.dumps(value)

    @property
    def details(self):
        if self._details is None:
            return None
        return json.loads(self._details)

    @details.setter
    def details(self, value):
        if value is None:
            self._details = None
        else:
            self._details = json.dumps(value)

    @property
    def input_params(self):
        return json.loads(self._input_params)

    @input_params.setter
    def input_params(self, value):
        self._input_params = json.dumps(value)
