from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from urllib.parse import unquote, quote
from dependencies.auth import verificar_token_http
import os
import fdb

router = APIRouter()

# Rota 1: Servir imagem local por caminho físico (protegida)
@router.get("/{data}/{tipo}/{arquivo:path}", dependencies=[Depends(verificar_token_http)])
def serve_imagem(data: str, tipo: str, arquivo: str):
    nome_arquivo = unquote(arquivo)
    caminho = f"/mnt/imagens/{data}/{tipo}/{nome_arquivo}"

    if not os.path.isfile(caminho):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    return FileResponse(path=caminho, media_type="image/jpeg")


# Rota 2: Buscar imagens vinculadas ao contrato (protegida)
@router.get("", dependencies=[Depends(verificar_token_http)])
def listar_imagens_por_contrato(contrato: int = Query(..., description="Número do contrato")):
    try:
        con = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/DIGITALIZADOR.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='ISO8859_1'
        )
        cur = con.cursor()

        query = """
        SELECT
            ri.REGISTRO_IMAGE,
            ri.REGISTRO,
            ri.TIPO_DOC,
            td.DESCR AS DESCR_TIPO_DOC,
            ri.FRENTE,
            ri.NR_FOLHA,
            ri.TOTAL_FOLHAS,
            ri.IMAGE,
            ri.IMAGE_THUMBNAIL,
            '' AS DATA,
            '' AS ARQUIVO
        FROM REGISTRO_IMAGE ri
        JOIN REGISTRO r ON r.REGISTRO = ri.REGISTRO
        JOIN TIPO_DOC td ON td.TIPO_DOC = ri.TIPO_DOC
        WHERE r.CONTRATO = ?
          AND ri.IMAGE IS NOT NULL
        ORDER BY UPPER(td.DESCR), ri.NR_FOLHA, ri.FRENTE, ri.REGISTRO_IMAGE
        """

        cur.execute(query, (contrato,))
        rows = cur.fetchall()
        colunas = [desc[0].lower() for desc in cur.description]

        imagens = []
        for row in rows:
            item = dict(zip(colunas, row))

            caminho_full = item["image"].strip() if item["image"] else ""

            partes_full = caminho_full.split("\\")
            if len(partes_full) >= 3:
                data_pasta = partes_full[1]
                nome_arquivo = partes_full[-1]
                encoded_full = quote(nome_arquivo)
                encoded_thm = quote("THM" + nome_arquivo)

                imagens.append({
                    "registro_image": item["registro_image"],
                    "registro": item["registro"],
                    "tipo_doc": item["tipo_doc"],
                    "descr_tipo_doc": item["descr_tipo_doc"],
                    "frente": item["frente"],
                    "nr_folha": item["nr_folha"],
                    "total_folhas": item["total_folhas"],
                    "data": data_pasta,
                    "arquivo": nome_arquivo,
                    "full": f"https://bonfim.malotedigital.com.br/api/imagens/{data_pasta}/FULL/{encoded_full}",
                    "thumb": f"https://bonfim.malotedigital.com.br/api/imagens/{data_pasta}/THM/{encoded_thm}",
                    "docnewideas": "N"
                })

        if not imagens:
            raise HTTPException(status_code=404, detail="Nenhuma imagem encontrada para este contrato")

        return imagens

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar imagens: {str(e)}")
