import oracledb

def get_connection():
    return oracledb.connect(
        user="xxxx",
        password="xxxxx",
        dsn="host:1521/ORCL"
    )
