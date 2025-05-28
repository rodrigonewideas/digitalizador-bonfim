import fdb
import os

def get_conexao_digitalizador():
    return fdb.connect(
        host=os.getenv("FIREBIRD_HOST"),
        database=os.path.join(os.getenv("FIREBIRD_PATH"), "DIGITALIZADOR.GDB"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD"),
        charset=os.getenv("FIREBIRD_CHARSET", "ISO8859_1")
    )

def get_conexao_pdv_bonfim():
    return fdb.connect(
        host=os.getenv("FIREBIRD_HOST"),
        database=os.path.join(os.getenv("FIREBIRD_PATH"), "PDV_BONFIM.GDB"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD"),
        charset=os.getenv("FIREBIRD_CHARSET", "ISO8859_1")
    )
