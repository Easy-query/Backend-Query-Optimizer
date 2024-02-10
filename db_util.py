import cx_Oracle


def get_connection():
    username = 'oracle'
    password = 'oracle'
    dsn = 'localhost:1521/orcl'

    conn = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    return conn
