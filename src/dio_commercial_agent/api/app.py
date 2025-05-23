from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from src.dio_commercial_agent.ioc import container
from src.dio_commercial_agent.api import chat_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_dishka(container=container, app=app)
    return app
