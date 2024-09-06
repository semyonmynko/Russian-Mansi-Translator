from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

from app.ml_models.translation_model import perform_translation
from app.schemas.translation import TranslationRequest, TranslationResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.dependencies import get_db

from app.crud.word import word
from app.schemas.word import Word
from app.crud.phrase import phrase
from app.schemas.phrase import Phrase

from app.crud.suggested_word import suggested_word
from app.schemas.suggested_word import SuggestedWordCreate
from app.crud.suggested_phrase import suggested_phrase
from app.schemas.suggested_phrase import SuggestedPhraseCreate

from app.auth import verify_token

app = FastAPI(title="Mansi translator API")#, dependencies=[Depends(verify_token)])

api_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Настраиваем Jinja2 для работы с шаблонами
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/")
def read_root(request: Request):
    # Рендерим шаблон index.html
    return templates.TemplateResponse("index.html", {"request": request})


@api_router.post("/translate", status_code=200, response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Эндпоинт перевода.
    """
    translated_text = perform_translation(request=request)
    print(translated_text)

    return TranslationResponse(translated_text=translated_text)


#===WORD===
@api_router.post("/add/word", status_code=201, response_model=Word)
async def add_word(
    *,
    db: Session = Depends(get_db),
    word_in: SuggestedWordCreate
):
    """
    Эндпоинт для добавления слова и его перевода.
    """
    try:
        return suggested_word.create(db=db, obj_in=word_in)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Integrity error, possible duplicate") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e


@api_router.get("/search/word", status_code=200, response_model=list[Word])
async def search_words(
    query: str, 
    language: str = Query(..., regex="^(mansi|russian)$"), 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для поиска слов по заданному запросу в указанном языке.
    """
    try:
        results = word.search(db, query=query, language=language, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return results



#===PHRASE===
@api_router.post("/add/phrase", status_code=201, response_model=Phrase)
async def add_phrase(
    *,
    db: Session = Depends(get_db),
    phrase_in: SuggestedPhraseCreate
):
    """
    Эндпоинт для добавления фразы и ее перевода.
    """
    try:
        return suggested_phrase.create(db=db, obj_in=phrase_in)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Integrity error, possible duplicate") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e


@api_router.get("/search/phrase", status_code=200, response_model=list[Phrase])
async def search_phrases(
    query: str, 
    language: str = Query(..., regex="^(mansi|russian)$"), 
    topic: str = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для поиска фраз по заданному запросу в указанном языке.
    """
    try:
        results = phrase.search(db, query=query, language=language, topic=topic, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return results


@api_router.get("/")
async def root():
    return {"message": "Welcome to the translation API"}


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")