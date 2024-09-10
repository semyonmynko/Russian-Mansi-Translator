from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
import os
from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForSeq2SeqLM

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
from app.settings import settings

app = FastAPI(title="Mansi translator API", static_folder='templates')#, dependencies=[Depends(verify_token)])

api_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Настраиваем Jinja2 для работы с шаблонами
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


@app.on_event("startup")
def get_translation(text: str) -> str:
    global onnx_translation
    to_onnx = '/home/gh58093lm/model_v1/'
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(to_onnx, "tokenizer"))
    model = ORTModelForSeq2SeqLM.from_pretrained(os.path.join(to_onnx, "model"))
    onnx_translation = pipeline("translation_ru_to_en", model=model, tokenizer=tokenizer)

    return onnx_translation


@app.get("/")
def read_root(request: Request = None):
    return templates.TemplateResponse("index.html", {"request": request, "api_token": settings.api_token})
    

@app.get("/add_translation")
def get_translation_page(type: str = Query(..., description="Type of translation page: 'word' or 'phrase'"), request: Request = None):
    if type == "word":
        return templates.TemplateResponse(f"add_translation/add_translation_word.html", {"request": request, "api_token": settings.api_token})
    elif type == "phrase":
        return templates.TemplateResponse(f"add_translation/add_translation_phrase.html", {"request": request, "api_token": settings.api_token})
    else:
        return {"error": "Invalid type. Use 'word' or 'phrase'."}


@app.get("/add_pop_up")
def get_pop_up_page(type: str = Query(..., description="Type of translation page: 'word' or 'phrase'"), request: Request = None):
    if type == "rate":
        return templates.TemplateResponse(f"pop-ups/pop_up_rate.html", {"request": request, "api_token": settings.api_token})
    elif type == "wrong":
        return templates.TemplateResponse(f"pop-ups/pop_up_wrong.html", {"request": request, "api_token": settings.api_token})
    else:
        return {"error": "Invalid type. Use 'word' or 'phrase'."}
    

@api_router.post("/translate", status_code=200, response_model=TranslationResponse, dependencies=[Depends(verify_token)])
async def translate_text(request: TranslationRequest):
    """
    Эндпоинт перевода.
    """
    translated_text = onnx_translation(request.text)
    print(translated_text)

    return TranslationResponse(translated_text=translated_text)


@app.get("/keyboard/{keyboard_type}", response_class=HTMLResponse)#, dependencies=[Depends(verify_token)])
async def load_keyboard(request: Request, keyboard_type: str):
    try:
        return templates.TemplateResponse(f"keyboard/keyboard-{keyboard_type}.html", {"request": request})
    except:
        return HTMLResponse(content="Keyboard not found", status_code=404)


#===WORD===
@api_router.post("/add/word", status_code=201, response_model=Word, dependencies=[Depends(verify_token)])
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


@api_router.get("/search/word", status_code=200, response_model=list[Word], dependencies=[Depends(verify_token)])
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
@api_router.post("/add/phrase", status_code=201, response_model=Phrase, dependencies=[Depends(verify_token)])
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


@api_router.get("/search/phrase", status_code=200, response_model=list[Phrase], dependencies=[Depends(verify_token)])
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


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")