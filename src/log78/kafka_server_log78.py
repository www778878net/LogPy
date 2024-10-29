import asyncio
from aiokafka import AIOKafkaProducer
import time
from typing import Optional
from log78.log_entry import LogEntry, BasicInfo

class KafkaServerLog78:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = None
        self._error_count = 0
        self._last_attempt_time = 0
        self._retry_interval = 300  # 5分钟 = 300秒

    @property
    def producer(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return self._producer

    async def start_producer(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self._producer.start()

    async def stop_producer(self):
        if self._producer is not None:
            await self._producer.stop()

    async def log_to_server(self, log_json: str):
        current_time = time.time()
        if self._error_count >= 2 and (current_time - self._last_attempt_time) < self._retry_interval:
            return  # 暂时不发送日志

        if (current_time - self._last_attempt_time) >= self._retry_interval:
            self._error_count = 0  # 重置错误计数

        try:
            await self.producer.send_and_wait(self.topic, log_json.encode('utf-8'))
            self._error_count = 0  # 成功发送后重置错误计数
        except Exception as e:
            self._error_count += 1
            self._last_attempt_time = current_time
            print(f"Error sending log to Kafka: {e}")

# 测试代码
if __name__ == "__main__":
    import asyncio

    async def test_kafka_log78():
        kafka_logger = KafkaServerLog78(bootstrap_servers='192.168.31.181:30008', topic='log-topic')
        await kafka_logger.start_producer()

        log_entry = LogEntry(basic=BasicInfo(summary="Test summarylogpy", message="Test message"))
        log_json = log_entry.to_json()

        await kafka_logger.log_to_server(log_json)
        await kafka_logger.stop_producer()

    asyncio.run(test_kafka_log78())    

