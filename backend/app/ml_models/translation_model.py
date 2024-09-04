from transformers import MarianMTModel, MarianTokenizer
from fastapi import HTTPException

from app.schemas.translation import TranslationRequest


def get_model_and_tokenizer(source_lang: str, target_lang: str):
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model loading failed: {str(e)}")
    return model, tokenizer


def perform_translation(request: TranslationRequest):

    model, tokenizer = get_model_and_tokenizer(request.source_lang, request.target_lang)
    inputs = tokenizer.encode(request.text, return_tensors="pt")
    translated = model.generate(inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return translated_text