from app.crud.base import CRUDBase
from app.models.suggested_phrase import SuggestedPhraseTranslation
from app.schemas.suggested_phrase import SuggestedPhraseCreate, SuggestedPhraseUpdate

class CRUDSuggestedPhrase(CRUDBase[SuggestedPhraseTranslation, SuggestedPhraseCreate, SuggestedPhraseUpdate]):
    pass

suggested_phrase = CRUDSuggestedPhrase(SuggestedPhraseTranslation)