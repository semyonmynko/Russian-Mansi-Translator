from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.phrase import PhraseTranslation
from app.schemas.phrase import PhraseCreate, PhraseUpdate

class CRUDPhrase(CRUDBase[PhraseTranslation, PhraseCreate, PhraseUpdate]):
    def search(self, db: Session, query: str, language: str, skip: int = 0, limit: int = 100):
        """
        Поиск фраз в зависимости от указанного языка.
        """
        if language == "mansi":
            filter_condition = self.model.mansi_phrase.ilike(f'%{query}%')
        elif language == "russian":
            filter_condition = self.model.russian_phrase.ilike(f'%{query}%')
        else:
            raise ValueError("Unsupported language. Choose 'mansi' or 'russian'.")

        return db.query(self.model).filter(filter_condition).offset(skip).limit(limit).all()

phrase = CRUDPhrase(PhraseTranslation)