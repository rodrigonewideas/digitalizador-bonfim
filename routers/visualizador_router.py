from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from dependencies.auth import verificar_token_http
from jose import JWTError, jwt
import os

router = APIRouter()

@router.post("/visualizador", response_class=HTMLResponse)
async def gerar_html_visualizador(request: Request):
    # Extrai o token do header Authorization
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou inválido")
    
    token = auth.split(" ")[1]

    try:
        # Verifica o token manualmente
        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM", "HS256")
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    body = await request.json()
    imagens = body.get("imagens", [])

    if not imagens:
        raise HTTPException(status_code=400, detail="Lista de imagens não fornecida")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Documentos Selecionados</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
            .grid {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .card {{
                background: white;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                width: 45%;
            }}
            .card img {{
                width: 100%;
                max-height: 400px;
                object-fit: contain;
                cursor: zoom-in;
            }}
        </style>
    </head>
    <body>
        <h1>Documentos Selecionados ({len(imagens)})</h1>
        <div class="grid">
    """

    for img in imagens:
        url = img.get("full", "")
        tipo = img.get("tipo_doc", "Documento")
        doc_id = img.get("registro_image", "")
        pos = img.get("posicao", "Pg ? / ?")
        contrato = img.get("contrato", "")
        html += f"""
            <div class="card">
                <h3>{tipo} ({doc_id})</h3>
                <p>{pos}</p>
                <img data-src="{url}" alt="Carregando..." />
                <p><strong>Contrato:</strong> {contrato}</p>
            </div>
        """

    html += f"""
        </div>
        <script>
        const token = "{token}";
        document.querySelectorAll("img[data-src]").forEach(async img => {{
            const url = img.getAttribute("data-src");
            try {{
                const res = await fetch(url, {{
                    headers: {{ Authorization: `Bearer ${{token}}` }}
                }});
                if (!res.ok) {{
                    img.alt = "Erro " + res.status;
                    return;
                }}
                const blob = await res.blob();
                img.src = URL.createObjectURL(blob);
            }} catch (err) {{
                img.alt = "Erro ao carregar imagem";
                console.error(err);
            }}
        }});
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
