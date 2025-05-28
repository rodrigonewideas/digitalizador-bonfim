import fdb

try:
    con = fdb.connect(
        host="192.168.5.232",  # ou 192.168.5.232 se esse for o correto
        database="C:/solution/data/PDV_BONFIM.GDB",
        user="SYSDBA",
        password="bonfim2005",
        charset="UTF8"
    )
    cur = con.cursor()
    lote = "1588"

    print(f"Executando consulta para lote {lote}")
    cur.execute("""
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
    """, (lote,))

    rows = cur.fetchall()
    print(f"Total encontrado: {len(rows)}")

    for r in rows:
        print(r)

    con.close()

except Exception as e:
    print("Erro:", e)
