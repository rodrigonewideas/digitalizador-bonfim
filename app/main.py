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
    title="📄 Digitalizador Bonfim API",
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
    allow_origin_regex=r"https://.*\.lovable\.app|https://bonfim\.malotedigital\.com\.br",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "cache-control"
    ],
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
