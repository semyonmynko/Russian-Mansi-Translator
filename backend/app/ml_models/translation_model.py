from fastapi import HTTPException

from app.schemas.translation import TranslationRequest


def get_model(source_lang: str, target_lang: str):
    model = []
    return model

def perform_translation(request: TranslationRequest):

    model = get_model(source_lang=request.source_lang, target_lang=request.target_lang)
    traslated_text = f'Translation from {request.source_lang} to {request.target_lang}'

    return traslated_text