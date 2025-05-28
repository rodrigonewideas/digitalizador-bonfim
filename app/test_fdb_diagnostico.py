import fdb

try:
    print("🔌 Conectando ao banco...")
    con = fdb.connect(
        host="192.168.5.232",  # Ajuste se necessário
        database="C:/solution/data/PDV_BONFIM.GDB",
        user="SYSDBA",
        password="bonfim2005",
        charset="UTF8"
    )
    cur = con.cursor()
    lote = "1588"
    print(f"🎯 Lote alvo: {lote}")

    # 1. Testar SELECT simples sem JOIN
    print("\n🧪 Teste 1: SELECT simples com WHERE NR_TERRENO = ?")
    cur.execute("SELECT FIRST 5 * FROM CONTRATO WHERE NR_TERRENO = ?", (lote,))
    for row in cur.fetchall():
        print("✅ Resultado:", row)

    # 2. Verificar se existem muitos registros com esse NR_TERRENO
    print("\n🧪 Teste 2: Contagem de registros com esse NR_TERRENO")
    cur.execute("SELECT COUNT(*) FROM CONTRATO WHERE NR_TERRENO = ?", (lote,))
    print("🔢 Quantidade encontrada:", cur.fetchone()[0])

    # 3. Tentar adicionar o primeiro JOIN
    print("\n🧪 Teste 3: SELECT com JOIN em CONTRATO_TITULAR")
    cur.execute("""
        SELECT FIRST 5
            c.CONTRATO,
            c.NR_CONTRATO,
            ct.DT_VENDA
        FROM CONTRATO c
        JOIN CONTRATO_TITULAR ct ON ct.CONTRATO = c.CONTRATO AND ct.RESP_PGTO = 'S'
        WHERE c.NR_TERRENO = ?
    """, (lote,))
    for row in cur.fetchall():
        print("✅ Parcial com JOIN ct:", row)

    # 4. Adicionar TITULAR e VENDEDOR em seguida se o anterior funcionar
    print("\n🧪 Teste 4: Consulta completa com todos os JOINs")
    cur.execute("""
        SELECT FIRST 5
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
    for row in cur.fetchall():
        print("✅ JOINs completos:", row)

    con.close()
    print("\n✅ Diagnóstico finalizado com sucesso.")

except Exception as e:
    print("❌ ERRO DETECTADO:")
    print(e)
