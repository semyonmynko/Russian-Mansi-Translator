from typing import Optional
from pydantic import BaseModel


class SuggestedWordBase(BaseModel):
    mansi_word: str
    russian_word: str
    part_of_speech: Optional[str] = None
    definition: Optional[str] = None

class SuggestedWordCreate(SuggestedWordBase):
    pass

class SuggestedWordUpdate(SuggestedWordBase):
    pass

class SuggestedWordInDBBase(SuggestedWordBase):
    id: int

    class Config:
        orm_mode = True

class SuggestedWord(SuggestedWordInDBBase):
    pass