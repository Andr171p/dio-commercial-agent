from langchain_core.embeddings import Embeddings

from langchain_pinecone import PineconeVectorStore

from ..constants import SERVICES_INDEX_NAME, PRICE_LIST_INDEX_NAME


class ServicesIndex(PineconeVectorStore):
    def __init__(
            self,
            pinecone_api_key: str,
            embedding: Embeddings,
            index_name: str = SERVICES_INDEX_NAME
    ) -> None:
        super().__init__(
            pinecone_api_key=pinecone_api_key,
            embedding=embedding,
            index_name=index_name
        )


class PriceListIndex(PineconeVectorStore):
    def __init__(
            self,
            pinecone_api_key: str,
            embedding: Embeddings,
            index_name: str = PRICE_LIST_INDEX_NAME
    ) -> None:
        super().__init__(
            pinecone_api_key=pinecone_api_key,
            embedding=embedding,
            index_name=index_name
        )
