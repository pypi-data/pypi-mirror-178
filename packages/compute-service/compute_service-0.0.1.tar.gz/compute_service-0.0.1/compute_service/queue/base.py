from contextlib import contextmanager
from contextvars import ContextVar
from typing import Union

from . import crud, capture_std


@contextmanager
def get_session(sessionmaker):
    session = sessionmaker()
    try:
        yield session
    finally:
        session.close()


task_uuid: ContextVar[str] = ContextVar('task_uuid')
task_session: ContextVar[str] = ContextVar('task_session')


class BaseQueue():
    """ Queue should allow submitting data for processing with handler
    """
    def __init__(self, *args, **kwargs):
        pass

    async def prepare(self):
        pass

    async def release(self):
        pass

    async def submit(self, task_data: Union[dict, str]):
        pass


class BaseHandler():
    """ Handler should wait for tasks from queue and process them with "task_callback"
    """
    def __init__(self, *args, **kwargs):
        pass
 
    def start(self):
        pass

    async def _process_task(self, task_data):
        uuid = task_data['uuid']
        print(f"Recieved new task: '{uuid}'")

        with get_session(self._session) as db:
            crud.start(db, uuid)

        task_uuid.set(uuid)
        task_session.set(self._session)

        try:
            with capture_std.capture_std():
                result = self._task_callback(task_data['input_params'])
        except Exception as e:
            with get_session(self._session) as db:
                crud.error(db, uuid, str(e))
            return

        with get_session(self._session) as db:
            if not isinstance(result, dict):
                crud.success(db, uuid, {'value': result})

            crud.success(db, uuid, result)


def report_details(details):
    with get_session(task_session.get()) as db:
        crud.details(db, task_uuid.get(), details)
