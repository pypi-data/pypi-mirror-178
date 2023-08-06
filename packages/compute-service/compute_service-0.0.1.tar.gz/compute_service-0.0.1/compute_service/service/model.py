from typing import Literal, Optional

from pydantic import BaseModel, root_validator


class LocalConfigModel(BaseModel):
    queue_socket: str


class KafkaConfigModel(BaseModel):
    bootstrap_servers: list[str]
    linger_ms: int
    topic: str
    group_id: str


class ServiceModel(BaseModel):
    queue: Literal['local', 'kafka', 'test']
    database_url: str
    local_config: LocalConfigModel
    kafka_config: KafkaConfigModel

    @root_validator
    def type_match(cls, values):
        if values.get('queue') == 'kafka' and values.get('kafka_config') is None:
            raise ValueError('queue = "kafka" require defined "kafka_config"')
        if values.get('queue') == 'local' and values.get('local_config') is None:
            raise ValueError('queue = "local" require defined "local_config"')
        return values
