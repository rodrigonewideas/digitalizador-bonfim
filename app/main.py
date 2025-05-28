from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.digitalizador_router import router as digitalizador_router, processar_lote
from routers.imagens_router import router as imagens_router
from dotenv import load_dotenv

load_dotenv()

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

# Middleware de CORS com suporte a subdomínios do Lovable e domínio fixo
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.lovable\.app|https://bonfim\.malotedigital\.com\.br",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de verificação (sem cabeçalho manual)
@app.get("/ping")
def health_check_ping():
    return {"success": True, "detail": "API funcionando"}

# Alias direto para /lote (sem cabeçalho manual)
@app.get("/lote")
def alias_lote(lote: str):
    return processar_lote(lote)

# Rotas com prefixos
app.include_router(digitalizador_router, prefix="/api/digitalizador")
app.include_router(imagens_router, prefix="/api/imagens")
