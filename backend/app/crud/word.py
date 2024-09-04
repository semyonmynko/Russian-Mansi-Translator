from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.word import WordTranslation
from app.schemas.word import WordCreate, WordUpdate

class CRUDWord(CRUDBase[WordTranslation, WordCreate, WordUpdate]):
    def search(self, db: Session, query: str, language: str, skip: int = 0, limit: int = 100):
        """
        Поиск слова в зависимости от указанного языка.
        """
        if language == "mansi":
            filter_condition = self.model.mansi_word == query
        elif language == "russian":
            filter_condition = self.model.russian_word == query
        else:
            raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        return db.query(self.model).filter(filter_condition).offset(skip).limit(limit).all()

word = CRUDWord(WordTranslation)