from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def get_model_and_tokenizer(source_lang: str, target_lang: str):
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model loading failed: {str(e)}")
    return model, tokenizer

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):

    model, tokenizer = get_model_and_tokenizer(request.source_lang, request.target_lang)
    
    inputs = tokenizer.encode(request.text, return_tensors="pt")

    translated = model.generate(inputs)

    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return TranslationResponse(translated_text=translated_text)

@app.get("/")
async def root():
    return {"message": "Welcome to the translation API"}
