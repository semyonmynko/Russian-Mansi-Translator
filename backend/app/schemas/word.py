from typing import Optional
from pydantic import BaseModel


class WordBase(BaseModel):
    mansi_word: str
    russian_word: str
    definition: Optional[str] = None

class WordCreate(WordBase):
    pass

class WordUpdate(WordBase):
    pass

class WordInDBBase(WordBase):
    id: int

    class Config:
        orm_mode = True

class Word(WordInDBBase):
    pass