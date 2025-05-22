import logging

from src.dio_commercial_agent.app import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()
