
from fastapi import FastAPI

from compute_service.default import DefaultSettings
from compute_service.api.config import APIConfig
from compute_service.api.database import get_engine, get_sessionmaker
from compute_service.api.models import Base
from compute_service.service.model import ServiceModel, LocalConfigModel, KafkaConfigModel
from compute_service.queue.base import report_details, BaseQueue
from compute_service.queue.kafka import KafkaHandler, KafkaQueue
from compute_service.queue.local import LocalHandler, LocalQueue


default = DefaultSettings()


class ComputeService():
    def __init__(
        self, *,
        queue: str = default.queue,
        database_url: str = default.database_url,
        local_queue_socket: str = default.local_queue_socket,
        kafka_bootstrap_servers: str = default.kafka_bootstrap_servers,
        kafka_linger_ms: int = default.kafka_linger_ms,
        kafka_topic: str = default.kafka_topic,
        kafka_group_id: str = default.kafka_group
    ):
        self._config = ServiceModel(
            queue=queue,
            database_url=database_url,
            local_config=LocalConfigModel(queue_socket=local_queue_socket),
            kafka_config=KafkaConfigModel(
                bootstrap_servers=kafka_bootstrap_servers,
                linger_ms=kafka_linger_ms,
                topic=kafka_topic,
                group_id=kafka_group_id
            ))


    def create_app(self, input_model, input_validator=None):
        app = FastAPI()

        if self._config.queue == 'local':
            queue = LocalQueue(self._config.local_config)
        elif self._config.queue == 'kafka':
            queue = KafkaQueue(self._config.kafka_config)
        elif self._config.queue == 'test':
            queue = BaseQueue()
        else:
            raise ValueError('Invalid queue:', self._config.queue)

        engine = get_engine(self._config.database_url)
        Base.metadata.create_all(engine)

        apiconfig = APIConfig()
        apiconfig.input_model = input_model
        apiconfig.input_validator = input_validator
        apiconfig.sessionmaker = get_sessionmaker(engine)
        apiconfig.queue = queue

        from compute_service.routers import tasks
        app.include_router(tasks.router, prefix="/api/v1.0/tasks")

        return app


    def report_task_details(self, details):
        report_details(details)


    def create_handler(self, task_callback):
        engine = get_engine(self._config.database_url)
        session = get_sessionmaker(engine)

        if self._config.queue == 'local':
            handler = LocalHandler(task_callback, session, self._config.local_config)
        elif self._config.queue == 'kafka':
            handler = KafkaHandler(task_callback, session, self._config.kafka_config)
        else:
            raise ValueError('Invalid queue:', self._config.queue)

        return handler
        