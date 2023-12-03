# En el archivo routes.py dentro de la carpeta app
from flask import render_template
from flask_ngrok import run_with_ngrok
from app import app
from .forms.registro import MiFormulario,control_numero_usuarios
from .forms.borrar import borrar_usuario
from .forms.edicion import editar_usuario
from .forms.consulta import consulta
from .forms.registro import registro

run_with_ngrok(app)  # Ruta externa

app.config['SECRET_KEY'] = 'una_clave_secreta'  # Debes cambiar esto por una clave segura
# Lista para almacenar los usuarios
usuarios = []

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


