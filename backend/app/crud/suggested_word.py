from app.crud.base import CRUDBase
from app.models.suggested_word import SuggestedWordTranslation
from app.schemas.suggested_word import SuggestedWordCreate, SuggestedWordUpdate

class CRUDSuggestedWord(CRUDBase[SuggestedWordTranslation, SuggestedWordCreate, SuggestedWordUpdate]):
    pass

suggested_word = CRUDSuggestedWord(SuggestedWordTranslation)