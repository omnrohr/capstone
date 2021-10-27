import os
# --------------------------------------------------------------------------------------#
# AUTH0 config.
# --------------------------------------------------------------------------------------#

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', '<your_auth0_domain>')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE', '<your _auth0_api>')

# --------------------------------------------------------------------------------------#
# Database config.
# --------------------------------------------------------------------------------------#
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', '<db_username>')
DB_PASSWORD = os.getenv('DB_PASSWORD', '<your_db_pasword>')
DB_NAME = os.getenv('DB_NAME', '<db name>')
DB_PATH = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

DEBUG = True
PORT = 5000
