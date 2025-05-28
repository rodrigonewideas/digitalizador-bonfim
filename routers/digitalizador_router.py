from fastapi import APIRouter
import fdb
import traceback

router = APIRouter()

# 🔍 Função reutilizável que executa a consulta SQL
def processar_lote(lote: str):
    try:
        print(f"🔍 Iniciando busca para o lote: {lote}")

        # Conexão com o banco Firebird
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
                "qtde_imagens": 0  # Será preenchido futuramente
            })

        con.close()
        return response or {"mensagem": "Nenhum resultado encontrado."}

    except Exception as e:
        print("❌ ERRO AO CONSULTAR LOTE:")
        traceback.print_exc()
        return {"erro": str(e)}

# 🔗 Rota de busca por lote
@router.get("/lote")
def buscar_por_lote(lote: str):
    return processar_lote(lote)
