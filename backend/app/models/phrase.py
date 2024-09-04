from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class PhraseTranslation(Base):

    id = Column(Integer, primary_key=True)
    mansi_phrase = Column(String, nullable=False)
    russian_phrase = Column(String, nullable=False)
