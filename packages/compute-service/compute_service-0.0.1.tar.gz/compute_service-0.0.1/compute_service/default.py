from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    api_server='127.0.0.1:8000'
    database_url: str = "sqlite:///./tasks.db"
    queue: str = 'kafka'
    local_queue_socket: str = '/tmp/compute_local_queue.sock'
    kafka_bootstrap_servers: list[str] = ['127.0.0.1:9092']
    kafka_linger_ms: int = 1000
    kafka_topic: str = 'compute-tasks'
    kafka_group: str = 'workers'

    class Config:
        env_file = ".env"

