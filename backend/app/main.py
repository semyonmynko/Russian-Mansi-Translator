from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from typing import List, Optional
import time
import torch
import os
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

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
def load_model():
    global model, tokenizer
    start_init_time = time.time()
    model_name = "/home/gh58093lm/model_checkpoint_v1/"
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model.eval()
    end_init_time = time.time()
    print(f"""
        Initialize time: {end_init_time - start_init_time:.3f}s
    """)

@app.get("/")
def read_root(request: Request = None):
    return templates.TemplateResponse("index.html", {"request": request, "api_token": settings.api_token})


@app.get("/dict")
def read_root(request: Request = None):
    return templates.TemplateResponse("dict.html", {"request": request, "api_token": settings.api_token})


@app.get("/links")
def read_root(request: Request = None):
    return templates.TemplateResponse("links.html", {"request": request, "api_token": settings.api_token})


@app.get("/thematic")
def read_root(request: Request = None):
    return templates.TemplateResponse("thematic.html", {"request": request, "api_token": settings.api_token})
    

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

    start_pred_time = time.time()
    sentence = request.text
    inputs = tokenizer(sentence, truncation=True, padding='max_length', max_length=128)
    input_ids = torch.tensor(inputs['input_ids']).unsqueeze(0)
    generated_ids = model.generate(input_ids, max_length=200, num_beams=5, early_stopping=True)

    pred = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    pred = pred.replace('__en__ ', '')
    end_pred_time = time.time()

    print(f"""
        Prediction time: {end_pred_time - start_pred_time:.3f}s
        Request: {sentence} -> Output: {pred}
    """)

    return TranslationResponse(translated_text=pred)


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
    query: Optional[str] = None,
    language: str = Query(..., regex="^(mansi|russian)$"), 
    topic: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для поиска фраз по заданному запросу в указанном языке.
    """
    if not query and not topic:
        raise HTTPException(status_code=400, detail="Either query or topic must be provided.")
    
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