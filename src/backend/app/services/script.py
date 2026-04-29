from sqlmodel import Session
from app.db import engine
from app.services.embedding import EmbeddingService

with Session(engine) as session:
    service = EmbeddingService(session)

    service.create_embedding("Virat Kohli is a cricketer", page_number=1)
    service.create_embedding("MS Dhoni is a captain", page_number=2)
    service.create_embedding("Python is a programming language", page_number=3)