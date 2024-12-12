import json

from aiokafka import AIOKafkaConsumer
from config.database import get_db
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from logger.logger_setting import logger
from src.applications.bet import BetService
from src.domain.addition.enum import EventStatus

app = FastAPI()

KAFKA_BROKER = "kafka:9093"
KAFKA_TOPIC = "events"
messages = []

consumer = AIOKafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER)


async def consume_messages():
    await consumer.start()
    try:
        async for msg in consumer:
            message_data = json.loads(msg.value)
            status = message_data.get("status")
            if status != EventStatus.ongoing:
                event_id = message_data.get("id")
                async with get_db() as session:
                    service = BetService(session)
                await service.change_bet_status(event_id, status)
                logger.info(f"Status was change for event {event_id}")
            cache_backend = FastAPICache.get_backend()
            await cache_backend.set(
                f"cache:message_{message_data['id']}", json.dumps(message_data)
            )

            logger.info(f"Message received and cached: {message_data}")
        return {"messages"}
    except Exception as e:
        logger.info(f"Error receiving messages: {str(e)}")
    finally:
        await consumer.stop()
