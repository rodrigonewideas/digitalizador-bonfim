import os
import fdb

def get_cessionarios_por_lote(nr_lote: str):
    try:
        # Conexão com PDV_BONFIM
        con = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/PDV_BONFIM.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='UTF8'
        )
        cur = con.cursor()

        # LOTE é do tipo CHAR(10) e CONTRATO é INTEGER
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
            JOIN CONTRATO_TITULAR ct ON ct.CONTRATO = c.CONTRATO
            JOIN TIPO_DOC 
            JOIN TITULAR t ON t.CODIGO = ct.TITULAR
            LEFT JOIN VENDEDOR v ON v.VENDEDOR = c.VENDEDOR
            WHERE c.NR_TERRENO LIKE ?
        """

        cur.execute(query, (f"%{nr_lote}%",))
        contratos = cur.fetchall()
        con.close()

        # Conexão com DIGITALIZADOR
        con_dig = fdb.connect(
            dsn='192.168.5.232:C:/solution/data/DIGITALIZADOR.GDB',
            user='SYSDBA',
            password='bonfim2005',
            charset='UTF8'
        )
        cur_dig = con_dig.cursor()

        resultado = []
        for row in contratos:
            contrato_id = row[0]  # INTEGER
            codigo = row[7]       # INTEGER

            # Busca o REGISTRO vinculado ao contrato
            cur_dig.execute("SELECT FIRST 1 REGISTRO FROM REGISTRO WHERE CONTRATO = ?", (contrato_id,))
            reg_row = cur_dig.fetchone()
            if reg_row:
                registro_id = reg_row[0]
                # Conta as imagens do REGISTRO
                cur_dig.execute("SELECT COUNT(*) FROM REGISTRO_IMAGE WHERE REGISTRO = ?", (registro_id,))
                count_row = cur_dig.fetchone()
                qtde_imagens = count_row[0] if count_row else 0
            else:
                qtde_imagens = 0

            resultado.append({
                "contrato": contrato_id,
                "nr_contrato": row[1].strip() if row[1] else "",
                "cessionario": row[2].strip() if row[2] else "",
                "data_venda": str(row[3])[:10] if row[3] else "",
                "vendedor": row[4].strip() if row[4] else "",
                "tipo_terreno": str(row[5]) if row[5] else "",
                "nr_terreno": row[6].strip() if row[6] else "",
                "codigo": codigo,
                "qtde_imagens": qtde_imagens
            })

        con_dig.close()
        return resultado

    except Exception as e:
        print(f"[ERRO CONEXAO_PDV] {e}")
        raise
