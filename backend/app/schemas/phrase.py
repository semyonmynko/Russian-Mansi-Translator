from typing import Optional
from pydantic import BaseModel


class PhraseBase(BaseModel):
    mansi_phrase: str
    russian_phrase: str

class PhraseCreate(PhraseBase):
    pass

class PhraseUpdate(PhraseBase):
    pass

class PhraseInDBBase(PhraseBase):
    id: int

    class Config:
        orm_mode = True

class Phrase(PhraseInDBBase):
    pass
