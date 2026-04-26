from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector
from .base import Base

class TextEmbedding(Base):
    __tablename__ = "text_embeddings"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    embedding = Column(Vector(1536))  
