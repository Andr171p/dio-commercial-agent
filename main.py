import logging

from src.dio_commercial_agent.api import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()
