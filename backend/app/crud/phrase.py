from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy.sql.expression import func as sql_func
from typing import Optional, List


from app.crud.base import CRUDBase
from app.models.phrase import PhraseTranslation
from app.schemas.phrase import PhraseCreate, PhraseUpdate

class CRUDPhrase(CRUDBase[PhraseTranslation, PhraseCreate, PhraseUpdate]):
    def search(
        self,
        db: Session,
        query: Optional[str],
        language: str,
        topic: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[PhraseTranslation]:
        """
        Регистронезависимый поиск фраз с возможной фильтрацией по теме.
        """
        if not query and not topic:
            raise ValueError("Either query or topic must be provided.")

        # Условие поиска по языку
        filter_condition = None
        if query:
            search_query = query.lower()
            if language == "mansi":
                filter_condition = func.lower(self.model.mansi_phrase).like(f"%{search_query}%")
            elif language == "russian":
                filter_condition = func.lower(self.model.russian_phrase).like(f"%{search_query}%")
            else:
                raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        # Если указана тема, добавляем фильтр по теме
        if topic:
            topic_condition = func.lower(self.model.topic).like(f"%{topic.lower()}%")
            if filter_condition is not None:
                filter_condition = and_(filter_condition, topic_condition)
            else:
                filter_condition = topic_condition

        # Выполняем запрос с фильтрацией и уникальными записями
        subquery = db.query(self.model).filter(filter_condition).distinct().subquery()
        
        # Выполняем запрос к подзапросу с случайной сортировкой
        query = db.query(self.model).from_statement(
            db.query(subquery).order_by(sql_func.random()).offset(skip).limit(limit).statement
        )
        
        return query.all()

phrase = CRUDPhrase(PhraseTranslation)
