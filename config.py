import os
from dotenv import load_dotenv

# Obtén la ruta absoluta del directorio actual
basedir = os.path.abspath(os.path.dirname(__file__))

# Carga las variables de entorno desde el archivo .env
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('mysql://', 'mysql+pymysql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGERDUTY_API_KEY = os.getenv('PAGERDUTY_API_KEY')
    PAGERDUTY_BASE_URL = 'https://api.pagerduty.com'
