import asyncio
import json
from redis.asyncio import Redis

redis = Redis(host="localhost", port=6379, decode_responses=True)
from app.config.logging import logger
STREAM_NAME = "user:stream"
GROUP_NAME = "user_group"
CONSUMER_NAME = "worker-2"


async def setup():
    try:
        await redis.xgroup_create(
            name=STREAM_NAME,
            groupname=GROUP_NAME,
            id="0",
            mkstream=True
        )
        logger.info("set up ready for consuming stream")
    except Exception:
        # group already exists
        pass


async def process_event(event, data):
    if event == "user_created":
        logger.info(f"👤 New user: {data}")

        # simulate work
        await asyncio.sleep(1)

        # example tasks:

        logger.info(f"📧 Send email {data.get('email')}")
        logger.info(f"📊 Update analytics {data.get('user_id')}")


async def consume():
    while True:
        response = await redis.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={STREAM_NAME: ">"},
            count=10,
            block=5000
        )
        logger.info("Stream response:", response)
        if not response:
            continue

        for stream, messages in response:
            logger.info(f" messages {messages}")
            for msg_id, msg in messages:
                event = msg["event"]
                data = json.loads(msg["data"])
                logger.info(f"received type {msg_id}  {type(data)}")
                try:
                    await process_event(event, data)

                    # ✅ mark as done
                    await redis.xack(STREAM_NAME, GROUP_NAME, msg_id)

                except Exception as e:
                    logger.info("❌ Error:", e)
                    # no ack → will retry later


async def main():
    await setup()
    await consume()


if __name__ == "__main__":
    asyncio.run(main())