from dishka import Provider, provide, Scope, from_context, make_async_container

from redis.asyncio import Redis as AsyncRedis

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from langgraph.checkpoint.base import BaseCheckpointSaver

from .infrastructure.llms.yandex_gpt import YandexGPTChatModel
from .infrastructure.checkpointers.redis import AsyncRedisCheckpointSaver
from .infrastructure.vector_store import ServicesIndex, PriceListIndex

from .agentic.orchestrator import CommercialAgent
from .agentic.agents.supervisor.nodes import SupervisorAgent, ConsultantAgent, PriceListAgent

from .core.base import AIAgent
from .settings import Settings
from .constants import YANDEX_GPT_MODEL, TOP_K


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_embeddings(self, config: Settings) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=config.embeddings.MODEL_NAME,
            model_kwargs=config.embeddings.MODEL_KWARGS,
            encode_kwargs=config.embeddings.ENCODE_KWARGS
        )

    @provide(scope=Scope.APP)
    def get_redis(self) -> AsyncRedis:
        return AsyncRedis()

    @provide(scope=Scope.APP)
    def get_model(self, config: Settings) -> BaseChatModel:
        return YandexGPTChatModel(
            api_key=config.yandex_gpt.API_KEY,
            folder_id=config.yandex_gpt.FOLDER_ID,
            model=YANDEX_GPT_MODEL
        )

    @provide(scope=Scope.APP)
    def get_checkpoint_saver(self, redis: AsyncRedis) -> BaseCheckpointSaver:
        return AsyncRedisCheckpointSaver(redis)

    @provide(scope=Scope.APP)
    def get_services_index(
        self,
        config: Settings,
        embeddings: Embeddings
    ) -> ServicesIndex:
        return ServicesIndex(
            pinecone_api_key=config.pinecone.API_KEY,
            embedding=embeddings,
        )

    @provide(scope=Scope.APP)
    def get_price_list_index(
            self,
            config: Settings,
            embeddings: Embeddings
    ) -> PriceListIndex:
        return PriceListIndex(
            pinecone_api_key=config.pinecone.API_KEY,
            embedding=embeddings
        )

    @provide(scope=Scope.APP)
    def get_consultant_agent(
            self,
            vector_store: ServicesIndex,
            model: BaseChatModel
    ) -> ConsultantAgent:
        return ConsultantAgent(
            vector_store=vector_store,
            model=model,
            top_k=TOP_K
        )

    @provide(scope=Scope.APP)
    def get_price_list_agent(
            self,
            vector_store: PriceListIndex,
            model: BaseChatModel
    ) -> PriceListAgent:
        return PriceListAgent(
            vector_store=vector_store,
            model=model,
            top_k=TOP_K
        )

    @provide(scope=Scope.APP)
    def get_supervisor_agent(self, model: BaseChatModel) -> SupervisorAgent:
        return SupervisorAgent(model)

    @provide(scope=Scope.APP)
    def get_ai_agent(
            self,
            supervisor: SupervisorAgent,
            consultant: ConsultantAgent,
            price_list: PriceListAgent,
            checkpoint_saver: BaseCheckpointSaver
    ) -> AIAgent:
        return CommercialAgent(
            supervisor=supervisor,
            consultant=consultant,
            price_list=price_list,
            checkpoint_saver=checkpoint_saver
        )


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
