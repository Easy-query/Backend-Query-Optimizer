import getpass
import cx_Oracle

pw = getpass.getpass('Enter password: ')

conn = cx_Oracle.connect(user='oracle', password=pw, dsn='localhost:1521/orcl')


def get_connection():
    return conn
