import asyncio
import logging
from uuid import uuid4

from src.dio_commercial_agent.ioc import container
from src.dio_commercial_agent.core.base import AIAgent


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    ai_agent = await container.get(AIAgent)
    chat_id = str(uuid4())
    while True:
        user_text = input("[User]: ")
        ai_text = await ai_agent.generate(chat_id, user_text)
        print(f"[AI]: {ai_text}")


if __name__ == "__main__":
    asyncio.run(main())
