from typing import List
from sqlmodel import Session

from aistory.voxabook.src.backend.app.models.text_embedding import TextEmbedding
from app.crud.embedding import embedding_crud


class EmbeddingService:
    def __init__(self, session: Session):
        self.session = session

    def generate_embedding(self, text: str) -> List[float]:
        from openai import OpenAI
        client = OpenAI()

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    def create_embedding(
        self,
        content: str,
        chapter_id: str | None = None,
        page_number: int | None = None,
    ):
        vector = self.generate_embedding(content)

        obj = TextEmbedding(
            text=content,
            embedding=vector,
        )

        return embedding_crud.create(instance=obj)
    
    def create_embedding(
        self,
        content: str,
        chapter_id: str | None = None,
        page_number: int | None = None,
    ):
        vector = self.generate_embedding(content)

        obj = Embedding(
            content=content,
            chapter_id=chapter_id,
            page_number=page_number,
            embedding=vector,
        )

        return embedding_crud.create(instance=obj)