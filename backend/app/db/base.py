# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.suggested_phrase import SuggestedPhraseTranslation  # noqa
from app.models.suggested_word import SuggestedWordTranslation  # noqa
from app.models.word import WordTranslation  # noqa
from app.models.phrase import PhraseTranslation  # noqa