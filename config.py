import os

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Opadah12')
DB_NAME = os.getenv('DB_NAME', 'casting_agency')
DB_PATH = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

DEBUG = True
PORT = 80
