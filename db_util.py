import sqlalchemy
from sqlalchemy.orm import sessionmaker

def get_connection():
    username = 'bakr'
    password = 'bakr'
    hostname = '34.31.91.76'
    port = '3306'
    database = 'optimisation_db'
    engine = sqlalchemy.create_engine('mysql+pymysql://' + username + ':' + password + '@' + hostname + ':' + port + '/' + database)
    session = sessionmaker(bind=engine)
    return session()
