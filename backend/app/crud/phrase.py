from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.phrase import PhraseTranslation
from app.schemas.phrase import PhraseCreate, PhraseUpdate

class CRUDPhrase(CRUDBase[PhraseTranslation, PhraseCreate, PhraseUpdate]):
    def search(self, db: Session, query: str, language: str, skip: int = 0, limit: int = 100):
        """
        Регистронезависимый поиск фраз в зависимости от указанного языка.
        """
        search_query = query.lower()  # Привести запрос к нижнему регистру

        if language == "mansi":
            filter_condition = func.lower(self.model.mansi_phrase).like(f"%{search_query}%")
        elif language == "russian":
            filter_condition = func.lower(self.model.russian_phrase).like(f"%{search_query}%")
        else:
            raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        return db.query(self.model).filter(filter_condition).offset(skip).limit(limit).all()

phrase = CRUDPhrase(PhraseTranslation)
