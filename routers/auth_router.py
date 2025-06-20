from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
import fdb
import os
from datetime import datetime, timedelta
from dependencies.auth import verificar_token_http

router = APIRouter()

# Configurações do token
SECRET_KEY = os.getenv("SECRET_KEY", "acarrocafazmaisbarulho")  # Substitua se quiser por valor do .env
ALGORITHM = "HS256"
TOKEN_EXPIRACAO_MINUTOS = int(os.getenv("TOKEN_EXPIRACAO_MINUTOS", "60"))

class LoginRequest(BaseModel):
    login: str
    senha: str

@router.get("/me")
def dados_usuario(payload=Depends(verificar_token_http)):
    return {
        "usuario": payload.get("sub"),
        "nome": payload.get("nome"),
        "admin": payload.get("admin", False)
    }

@router.post("/login")
def login_usuario(data: LoginRequest):
    try:
        con = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/DIGITALIZADOR.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='UTF8'
        )
        cur = con.cursor()

        cur.execute("""
    SELECT FONE2, NOME, ADMINISTRADOR 
    FROM USUARIO 
    WHERE UPPER(LOGIN) = ?
    """, (data.login.strip().upper().ljust(20),))

        
        row = cur.fetchone()
        con.close()

        if not row:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        senha_db, nome, administrador = row

        if data.senha.strip() != senha_db.strip():
            raise HTTPException(status_code=401, detail="Senha incorreta")

        expiracao = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRACAO_MINUTOS)
        token_data = {
            "sub": data.login.strip(),
            "nome": nome.strip() if nome else "",
            "admin": administrador.strip().upper() == "S",
            "exp": expiracao
        }

        token_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": token_jwt,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
