import asyncio
import logging
from uuid import uuid4

from src.dio_commercial_agent.ioc import container
from src.dio_commercial_agent.core.base import AIAgent
from src.dio_commercial_agent.core.entities import UserMessage


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    ai_agent = await container.get(AIAgent)
    chat_id = str(uuid4())
    while True:
        user_text = input("[User]: ")
        user_message = UserMessage(chat_id=chat_id, text=user_text)
        ai_message = await ai_agent.generate(user_message)
        print(f"[AI]: {ai_message.text}")


if __name__ == "__main__":
    asyncio.run(main())
