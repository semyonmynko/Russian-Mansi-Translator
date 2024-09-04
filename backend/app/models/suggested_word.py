from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class SuggestedWordTranslation(Base):

    id = Column(Integer, primary_key=True)
    mansi_word = Column(String, nullable=False)
    russian_word = Column(String, nullable=False)
    part_of_speech = Column(String, nullable=True)
    definition = Column(Text, nullable=True)
