# En el archivo __init__.py dentro de la carpeta app

from flask import Flask
from flask_ngrok import run_with_ngrok
import secrets
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)   # Reemplaza con una cadena segura y única
run_with_ngrok(app)  # Ruta externa

from app import routes


