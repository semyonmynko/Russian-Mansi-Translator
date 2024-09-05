from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.settings import settings


token_auth_scheme = HTTPBearer()

# Функция для проверки токена
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    if credentials.credentials != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token"
        )