from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import func as sql_func

from app.crud.base import CRUDBase
from app.models.word import WordTranslation
from app.schemas.word import WordCreate, WordUpdate

class CRUDWord(CRUDBase[WordTranslation, WordCreate, WordUpdate]):
    def search(self, db: Session, query: str, language: str, skip: int = 0, limit: int = 100):
        """
        Регистронезависимый поиск слова в зависимости от указанного языка.
        """
        search_query = query.lower()  # Привести запрос к нижнему регистру

        if language == "mansi":
            filter_condition = func.lower(self.model.mansi_word).like(f"%{search_query}%")
        elif language == "russian":
            filter_condition = func.lower(self.model.russian_word).like(f"%{search_query}%")
        else:
            raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        # Создаем подзапрос с фильтрацией и уникальными записями
        subquery = db.query(self.model).filter(filter_condition).distinct().subquery()

        # Выполняем запрос к подзапросу с случайной сортировкой
        query = db.query(self.model).from_statement(
            db.query(subquery).order_by(sql_func.random()).offset(skip).limit(limit).statement
        )

        return query.all()

word = CRUDWord(WordTranslation)