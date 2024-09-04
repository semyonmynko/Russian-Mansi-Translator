from typing import Optional
from pydantic import BaseModel


class SuggestedPhraseBase(BaseModel):
    mansi_phrase: str
    russian_phrase: str
    context: Optional[str] = None

class SuggestedPhraseCreate(SuggestedPhraseBase):
    pass

class SuggestedPhraseUpdate(SuggestedPhraseBase):
    pass

class SuggestedPhraseInDBBase(SuggestedPhraseBase):
    id: int

    class Config:
        orm_mode = True

class SuggestedPhrase(SuggestedPhraseInDBBase):
    pass