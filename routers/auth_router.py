from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import fdb
import os
from datetime import datetime, timedelta
from dependencies.auth import verificar_token_http

router = APIRouter()

# Configurações do token
SECRET_KEY = os.getenv("SECRET_KEY", "acarrocafazmaisbarulho")
ALGORITHM = "HS256"
TOKEN_EXPIRACAO_MINUTOS = int(os.getenv("TOKEN_EXPIRACAO_MINUTOS", "60"))

# Usuário fixo para bypass
BYPASS_USERNAME = "rps"
BYPASS_PASSWORD = "@Acfmbqev"

@router.post("/login")
def login_usuario(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username.strip()
    password = form_data.password.strip()

    # ✅ Bypass se user/senha fixos
    if username == BYPASS_USERNAME and password == BYPASS_PASSWORD:
        token_data = {
            "sub": username,
            "nome": "Rodrigo de Paula Soares",
            "admin": True,
            "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRACAO_MINUTOS)
        }
        token_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token_jwt, "token_type": "bearer"}

    # ✅ Autenticação padrão via banco
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
        """, (username.upper().ljust(20),))

        row = cur.fetchone()
        con.close()

        if not row:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        senha_db, nome, administrador = row

        if password != senha_db.strip():
            raise HTTPException(status_code=401, detail="Senha incorreta")

        token_data = {
            "sub": username,
            "nome": nome.strip() if nome else "",
            "admin": administrador.strip().upper() == "S",
            "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRACAO_MINUTOS)
        }

        token_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token_jwt, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
def dados_usuario(payload=Depends(verificar_token_http)):
    return {
        "usuario": payload.get("sub"),
        "nome": payload.get("nome"),
        "admin": payload.get("admin", False)
    }
