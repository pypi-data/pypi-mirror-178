import asyncio
import json
from contextvars import ContextVar
from typing import Union

from compute_service.service.model import LocalConfigModel
from .base import BaseHandler, BaseQueue
from .socketqueue import UnixSocketQueue


task_uuid: ContextVar[str] = ContextVar('task_uuid')
task_session: ContextVar[str] = ContextVar('task_session')


class LocalQueue(BaseQueue):
    def __init__(self, local_config: LocalConfigModel):
        self._local_config = local_config
        self._queue = UnixSocketQueue(socket_path=local_config.queue_socket)
        self._server_task = None

    async def prepare(self):
        if self._server_task is not None:
            raise ValueError('LocalQueue was already prepared')
        
        self._server_task = asyncio.create_task(self._queue.start_server())

    async def release(self):
        if self._server_task is None:
            raise ValueError('LocalQueue was not prepared')
        
        self._server_task.cancel()

    async def submit(self, task_data: Union[dict, str]):
        if isinstance(task_data, dict):
            await self._queue.submit(json.dumps(task_data).encode('utf-8'))
        elif isinstance(task_data, str):
            await self._queue.submit(task_data.encode('utf-8'))


class LocalHandler(BaseHandler):
    def __init__(self, task_callback: callable, session, local_config: LocalConfigModel):
        if not callable(task_callback):
            raise Exception("task_callback is not a function")

        self._task_callback = task_callback
        self._session = session
        self._local_config = local_config
        self._queue = UnixSocketQueue(socket_path=local_config.queue_socket)
 
    def start(self):
        print("Start handling tasks from local queue '{}'".format(
            self._local_config.queue_socket,
        ))
        asyncio.run(self._handle_tasks())
    
    async def _handle_tasks(self):
        while True:
            data = await self._queue.get()
            if data is None:
                await asyncio.sleep(1)
                continue
            task_data = json.loads(data.decode())
            await self._process_task(task_data)
