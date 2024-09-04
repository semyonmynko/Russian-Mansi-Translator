from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class WordTranslation(Base):

    id = Column(Integer, primary_key=True)
    mansi_word = Column(String, nullable=False)
    russian_word = Column(String, nullable=False)
    definition = Column(Text, nullable=True)