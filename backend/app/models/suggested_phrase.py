from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class SuggestedPhraseTranslation(Base):

    id = Column(Integer, primary_key=True)
    mansi_phrase = Column(String, nullable=False)
    russian_phrase = Column(String, nullable=False)
    context = Column(Text, nullable=True)
