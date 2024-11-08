import asyncio
from aiokafka import AIOKafkaProducer
import time
from typing import Any, Dict, List
from log78.log_entry import LogEntry, BasicInfo
from log78.iserver_log78 import IServerLog78

class KafkaServerLog78(IServerLog78):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = None
        self._producer_started = False  # 标志生产者是否已启动
        self._error_count = 0
        self._last_attempt_time = 0
        self._retry_interval = 300  # 5分钟 = 300秒

    @property
    def producer(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return self._producer
    
    async def log_batch_to_server(self, log_json_list: List[str]):
        """没有用要从logger78中改过来"""
        current_time = time.time()
        if self._error_count >= 2 and (current_time - self._last_attempt_time) < self._retry_interval:
            print("Skipping log due to retry interval")
            return  # 暂时不发送日志

        if (current_time - self._last_attempt_time) >= self._retry_interval:
            self._error_count = 0  # 重置错误计数

        try:
            if not self._producer_started:
                await self.start_producer()
            await self.producer.send_batch(
                [(self.topic, log_json.encode('utf-8')) for log_json in log_json_list]
            )
            self._error_count = 0  # 成功发送后重置错误计数
            #print("Batch logs sent to Kafka successfully")
        except Exception as e:
            self._error_count += 1
            self._last_attempt_time = current_time
            print(f"Error sending batch logs to Kafka: {e}")

    async def start_producer(self):
        if not self._producer_started:
            await self.producer.start()
            self._producer_started = True
            print("Kafka producer started")

    async def log_to_server(self, log_json: str):
        current_time = time.time()
        if self._error_count >= 2 and (current_time - self._last_attempt_time) < self._retry_interval:
            print("Skipping log due to retry interval")
            return  # 暂时不发送日志

        if (current_time - self._last_attempt_time) >= self._retry_interval:
            self._error_count = 0  # 重置错误计数

        try:
            if not self._producer_started:
                await self.start_producer()
            await self.producer.send_and_wait(self.topic, log_json.encode('utf-8'))
            self._error_count = 0  # 成功发送后重置错误计数
            #print("Log sent to Kafka successfully")
        except Exception as e:
            self._error_count += 1
            self._last_attempt_time = current_time
            print(f"Error sending log to Kafka: {e}")

    def server_url(self) -> str:
        return self.bootstrap_servers

# 示例使用
if __name__ == "__main__":
    async def test_kafka_log78():
        kafka_logger = KafkaServerLog78(bootstrap_servers='192.168.31.181:30008', topic='log-topic')

        log_entry = LogEntry(basic=BasicInfo(summary="Test summarylogpy", message="Test message"))
        log_json = log_entry.to_json()

        await kafka_logger.log_to_server(log_json)

    asyncio.run(test_kafka_log78())