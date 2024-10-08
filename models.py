from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    source_url = Column(String(255), unique=True, nullable=False)
    category = Column(String(100))  # Category after classification (e.g., Terrorism, Natural Disaster)
