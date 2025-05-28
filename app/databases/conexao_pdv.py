import fdb
import os

def get_cessionarios_por_lote(nr_lote: str):
    try:
        con = fdb.connect(
            dsn='192.168.5.232:/C:/solution/data/PDV_BONFIM.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='UTF8'
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
            WHERE c.NR_TERRENO LIKE ?
        """

        cur.execute(query, (f"%{nr_lote}%",))
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append({
                "contrato_id": row[0],
                "nr_contrato": row[1].strip() if row[1] else "",
                "cessionario": row[2].strip() if row[2] else "",
                "dt_venda": row[3].strftime("%Y-%m-%d") if row[3] else "",
                "vendedor": row[4].strip() if row[4] else "",
                "tipo_terreno": row[5],
                "nr_terreno": row[6].strip() if row[6] else "",
                "codigo_titular": row[7]
            })

        return resultado

    except Exception as e:
        print(f"[ERRO CONEXAO_PDV] {e}")
        return []
