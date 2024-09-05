from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.crud.base import CRUDBase
from app.models.phrase import PhraseTranslation
from app.schemas.phrase import PhraseCreate, PhraseUpdate

class CRUDPhrase(CRUDBase[PhraseTranslation, PhraseCreate, PhraseUpdate]):
    def search(self, db: Session, query: str, language: str, topic: str = None, skip: int = 0, limit: int = 100):
        """
        Регистронезависимый поиск фраз с возможной фильтрацией по теме.
        """
        search_query = query.lower()

        # Условие поиска по языку
        if language == "mansi":
            filter_condition = func.lower(self.model.mansi_phrase).like(f"%{search_query}%")
        elif language == "russian":
            filter_condition = func.lower(self.model.russian_phrase).like(f"%{search_query}%")
        else:
            raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        # Если указана тема, добавляем фильтр по теме
        if topic:
            filter_condition = and_(filter_condition, func.lower(self.model.topic).like(f"%{topic.lower()}%"))

        # Выполняем запрос с фильтрацией
        return db.query(self.model).filter(filter_condition).offset(skip).limit(limit).all()

phrase = CRUDPhrase(PhraseTranslation)
