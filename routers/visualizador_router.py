# Arquivo 1: routers/visualizador_router.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from dependencies.auth import verificar_token_http

router = APIRouter()

@router.post("/visualizador", response_class=HTMLResponse, dependencies=[Depends(verificar_token_http)])
async def gerar_html_visualizador(request: Request):
    body = await request.json()
    imagens = body.get("imagens", [])

    if not imagens:
        raise HTTPException(status_code=400, detail="Lista de imagens não fornecida")

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Documentos Selecionados</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .grid { display: flex; flex-wrap: wrap; gap: 20px; }
            .card {
                background: white;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                width: 45%;
            }
            .card img {
                width: 100%;
                max-height: 400px;
                object-fit: contain;
                cursor: zoom-in;
            }
        </style>
    </head>
    <body>
        <h1>Documentos Selecionados</h1>
        <div class="grid">
    """

    for img in imagens:
        img_url = img.get("full", "")
        contrato = img.get("contrato", "")
        doc_id = img.get("registro_image", "")
        html += f"""
            <div class=\"card\">
                <img src=\"{img_url}\" alt=\"Imagem não carregada\">
                <p><strong>Documento ID:</strong> {doc_id}<br><strong>Contrato:</strong> {contrato}</p>
            </div>
        """

    html += "</div></body></html>"
    return HTMLResponse(content=html)


# Arquivo 2: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from routers.digitalizador_router import router as digitalizador_router, processar_lote
from routers.imagens_router import router as imagens_router
from routers.auth_router import router as auth_router
from routers.visualizador_router import router as visualizador_router
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

app = FastAPI(
    title="\ud83d\udcc4 Digitalizador Bonfim API",
    description="API para consulta de contratos e imagens digitalizadas (Firebird)",
    version="1.0.0",
    contact={
        "name": "Rodrigo de Paula Soares",
        "email": "soares@niti.com.br",
        "url": "https://github.com/rodrigonewideas"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\\.lovable\\.app|https://bonfim\\.malotedigital\\.com\\.br",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/ping")
def health_check_ping():
    return {"success": True, "detail": "API funcionando"}

@app.get("/lote")
def alias_lote(lote: str):
    return processar_lote(lote)

app.include_router(digitalizador_router, prefix="/api/digitalizador")
app.include_router(imagens_router, prefix="/api/imagens")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(visualizador_router, prefix="/api/visualizador")
