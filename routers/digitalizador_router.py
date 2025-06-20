from fastapi import APIRouter, Depends
import fdb
import traceback
import unicodedata
from dependencies.auth import verificar_token_http

router = APIRouter()

# 🔠 Normaliza texto para ignorar acentos e case (usado em pós-processamento)
def normalizar(texto):
    if not texto:
        return ""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').upper()

# 🔍 Função reutilizável que executa a consulta SQL por lote
def processar_lote(lote: str):
    try:
        print(f"🔍 Iniciando busca para o lote: {lote}")

        con = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/PDV_BONFIM.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='ISO8859_1'
        )
        cur = con.cursor()

        query = """
            SELECT
                c.CONTRATO,
                c.NR_CONTRATO,
                t.RAZAO,
                ct.DT_VENDA,
                v.NOME,
                c.TIPO_TERRENO,
                c.NR_TERRENO,
                t.CODIGO
            FROM CONTRATO c
            JOIN CONTRATO_TITULAR ct ON ct.CONTRATO = c.CONTRATO AND ct.RESP_PGTO = 'S'
            JOIN TITULAR t ON t.CODIGO = ct.TITULAR
            LEFT JOIN VENDEDOR v ON v.VENDEDOR = c.VENDEDOR
            WHERE c.NR_TERRENO = ?
        """

        cur.execute(query, (lote,))
        results = cur.fetchall()

        response = []
        for row in results:
            response.append({
                "contrato": row[0],
                "nr_contrato": row[1].strip() if row[1] else "",
                "cessionario": row[2].strip() if row[2] else "",
                "data_venda": row[3],
                "vendedor": row[4].strip() if row[4] else "",
                "tipo_terreno": row[5],
                "nr_terreno": row[6].strip() if row[6] else "",
                "codigo": row[7],
                "qtde_imagens": 0
            })

        con.close()
        return response or {"mensagem": "Nenhum resultado encontrado."}

    except Exception as e:
        print("❌ ERRO AO CONSULTAR LOTE:")
        traceback.print_exc()
        return {"erro": str(e)}

# 🔍 Função para buscar por nome do cessionário (com acento-insensitive)
def processar_cessionario(nome: str):
    try:
        print(f"🔍 Iniciando busca para o cessionário: {nome}")

        con = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/PDV_BONFIM.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='ISO8859_1'
        )
        cur = con.cursor()

        query = """
            SELECT
                c.CONTRATO,
                c.NR_CONTRATO,
                t.RAZAO,
                ct.DT_VENDA,
                v.NOME,
                c.TIPO_TERRENO,
                c.NR_TERRENO,
                t.CODIGO
            FROM CONTRATO c
            JOIN CONTRATO_TITULAR ct ON ct.CONTRATO = c.CONTRATO AND ct.RESP_PGTO = 'S'
            JOIN TITULAR t ON t.CODIGO = ct.TITULAR
            LEFT JOIN VENDEDOR v ON v.VENDEDOR = c.VENDEDOR
        """

        cur.execute(query)
        results = cur.fetchall()

        nome_normalizado = normalizar(nome)
        response = []
        for row in results:
            razao = row[2].strip() if row[2] else ""
            if nome_normalizado in normalizar(razao):
                response.append({
                    "contrato": row[0],
                    "nr_contrato": row[1].strip() if row[1] else "",
                    "cessionario": razao,
                    "data_venda": row[3],
                    "vendedor": row[4].strip() if row[4] else "",
                    "tipo_terreno": row[5],
                    "nr_terreno": row[6].strip() if row[6] else "",
                    "codigo": row[7],
                    "qtde_imagens": 0
                })

        con.close()
        return response or {"mensagem": "Nenhum resultado encontrado."}

    except Exception as e:
        print("❌ ERRO AO CONSULTAR CESSIONÁRIO:")
        traceback.print_exc()
        return {"erro": str(e)}

# 🔗 Rota de busca por número do lote (proteção JWT)
@router.get("/lote", dependencies=[Depends(verificar_token_http)])
def buscar_por_lote(lote: str):
    return processar_lote(lote)

# 🔗 Rota de busca por nome do cessionário (proteção JWT)
@router.get("/cessionario", dependencies=[Depends(verificar_token_http)])
def buscar_por_cessionario(nome: str):
    return processar_cessionario(nome)
