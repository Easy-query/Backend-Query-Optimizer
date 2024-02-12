import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values


def get_connection():
    username = dotenv_values(".env")['USERNAME']
    password = dotenv_values(".env")['PASSWORD']
    hostname = dotenv_values(".env")['HOSTNAME']
    port = dotenv_values(".env")['PORT']
    database = dotenv_values(".env")['DATABASE']
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://' + username + ':' + password + '@' + hostname + ':' + port + '/' + database)
    session = sessionmaker(bind=engine)
    return session()
