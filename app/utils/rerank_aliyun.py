import asyncio
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from app.core.log_config import logger
from app.core.config import settings
from langchain.schema import Document
from dashscope import TextReRank
from typing import Optional, Sequence
from langchain_core.callbacks import Callbacks
def documents_to_list(documents: Sequence[Document]):
    return [doc.page_content for doc in documents]

def list_to_documents(doc_list):
    return [Document(page_content=content) for content in doc_list]

class RerankerWithBar:
    @staticmethod
    async def base_text_rerank(documents: list[str], query: str, top_n: int = 10):
        loop = asyncio.get_running_loop()
        logger.debug(f"Reranking {len(documents)} documents by aliyun")
        with ThreadPoolExecutor() as pool:
            resp = await loop.run_in_executor(
                pool,
                lambda: TextReRank().call(
                    model=TextReRank.Models.gte_rerank,
                    documents=documents,
                    query=query,
                    top_n=top_n,
                    return_documents=True,
                    api_key=settings.DASHSCOPE_API_KEY
                )
            )
        if resp.status_code == HTTPStatus.OK:
            logger.debug(f"Reranking done: {len(resp.output['results'])} documents")
            return resp.output["results"]
        else:
            logger.error(f"Error in reranking: {resp.message}")
            return []

    async def compress_documents(
            self,
            documents: Sequence[Document],
            query: str,
            bar: float = 0.3,
            callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        if len(documents) in [0,1]:
            return documents
        input_docs = documents_to_list(documents)
        reranked_results = await self.base_text_rerank(input_docs, query)
        if reranked_results:
            result = [documents[res.index] for res in reranked_results if res.relevance_score >= bar]
        else:
            result = documents
        return result

RerankerCompressor = RerankerWithBar()