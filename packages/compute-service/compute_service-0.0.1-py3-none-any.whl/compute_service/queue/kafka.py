import asyncio
import json
from typing import Union

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from compute_service.service.model import KafkaConfigModel
from .base import BaseHandler, BaseQueue


class KafkaQueue(BaseQueue):
    def __init__(self, kafka_config: KafkaConfigModel):
        self._kafka_config = kafka_config
        self._aioproducer = AIOKafkaProducer(
            bootstrap_servers=self._kafka_config.bootstrap_servers,
            value_serializer=lambda v: v.encode('utf-8'),
            acks='all',
            linger_ms=self._kafka_config.linger_ms)

    async def prepare(self):
        await self._aioproducer.start()

    async def release(self):
        await self._aioproducer.stop()

    async def submit(self, task_data: Union[dict, str]):
        if isinstance(task_data, dict):
            await self._aioproducer.send_and_wait(self._kafka_config.topic, json.dumps(task_data))
        elif isinstance(task_data, str):
            await self._aioproducer.send_and_wait(self._kafka_config.topic, task_data)


class KafkaHandler(BaseHandler):
    def __init__(self, task_callback: callable, session, kafka_config: KafkaConfigModel):
        if not callable(task_callback):
            raise Exception("task_callback is not a function")

        self._task_callback = task_callback
        self._session = session
        self._kafka_config = kafka_config
 
    def start(self):
        print("Start handling tasks from kafka '{}', topic '{}' with group '{}'".format(
            self._kafka_config.bootstrap_servers,
            self._kafka_config.topic,
            self._kafka_config.group_id
        ))
        asyncio.run(self._handle_tasks())
    
    async def _handle_tasks(self):
        consumer = AIOKafkaConsumer(
            self._kafka_config.topic,
            bootstrap_servers=self._kafka_config.bootstrap_servers,
            group_id=self._kafka_config.group_id,
            value_deserializer=lambda s: json.loads(s),
            auto_offset_reset='earliest'
        )

        await consumer.start()
        try:
            async for msg in consumer:
                await self._process_task(msg.value)
        finally:
            await consumer.stop()
