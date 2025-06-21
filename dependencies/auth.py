from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

# 🔐 Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "acarrocafazmaisbarulho")
ALGORITHM = "HS256"

# 🔐 Esquema de autenticação Bearer
bearer_scheme = HTTPBearer()

# ✅ Verifica se o token é válido
def verificar_token_http(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

# ✅ Verifica se o usuário autenticado é administrador
def verificar_admin(payload=Depends(verificar_token_http)):
    if not payload.get("admin"):
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return payload
