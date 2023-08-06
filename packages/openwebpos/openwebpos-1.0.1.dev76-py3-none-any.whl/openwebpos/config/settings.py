import os
from os import getenv

SECRET_KEY = getenv('SECRET_KEY', 'dev-key')
DEBUG = getenv('DEBUG', False)
TESTING = getenv('TESTING', False)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# database
DB_DIALECT = getenv('DB_DIALECT', 'sqlite')
DB_DRIVER = getenv('DB_DRIVER', None)
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT', None)
DB_NAME = getenv('DB_NAME')

if DB_DIALECT == 'sqlite':
    db_uri = DB_DIALECT + ':///' + os.path.join(os.getcwd(), 'instance',
                                                'openwebpos.db')
else:
    if DB_DRIVER:
        if DB_PORT:
            db_uri = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME} '
        else:
            db_uri = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    else:
        if DB_PORT:
            db_uri = f'{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        else:
            db_uri = f'{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG_TB_INTERCEPT_REDIRECTS = False
