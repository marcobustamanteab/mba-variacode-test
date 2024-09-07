from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde .env

def create_app(config_name=None):
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello, World!"
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
