# En el archivo routes.py dentro de la carpeta app
import json
from flask import render_template, request,flash,session,redirect, url_for
from flask_ngrok import run_with_ngrok
from app import app
from .forms.forms import MiFormulario  # Ajustando la importación de MiFormulario
from .forms.forms import control_numero_usuarios
import json
import os

run_with_ngrok(app)  # Ruta externa
app.config['SECRET_KEY'] = 'una_clave_secreta'  # Debes cambiar esto por una clave segura
# Lista para almacenar los usuarios
usuarios = []

@app.route('/')
def formulario():
    formulario = MiFormulario()
    try:
        usuarios_dir = 'usuarios'
        usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')

        if control_numero_usuarios():
            with open(usuarios_file, 'r') as file:
                usuarios = json.load(file)
        else:
            usuarios = []

    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        usuarios = []

    return render_template('formulario.html', formulario=formulario,usuarios=usuarios)

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    formulario = MiFormulario(request.form)
    try:
        if formulario.validate():
            #try:
                # Aquí puedes acceder a los datos del formulario
                nombre = formulario.nombre.data
                email = formulario.email.data
                apellidos = formulario.apellidos.data
                contrasena = formulario.contrasena.data
                telefono = formulario.telefono.data
                edad = formulario.edad.data

                # Construir un diccionario con los datos
                usuario = {
                    'nombre': nombre,
                    'email': email,
                    'apellidos': apellidos,
                    'contrasena': contrasena,
                    'telefono': telefono,
                    'edad':edad
                }
                guardar_usuario(usuario)

                # Puedes hacer algo con los datos, como almacenarlos en una base de datos
                flash("Formulario procesado correctamente.", 'success')
                  # Reiniciar el formulario para el próximo usuario
                return redirect(url_for('formulario'))
        else:
            flash("Error en el formulario. Por favor, verifica los datos.", 'danger')
            session.pop('error_flash_shown', None)
            return render_template('formulario.html', formulario=formulario)
        # Limpiar completamente todos los mensajes en la sesión
        session.clear()
        # Limpiar los mens  ajes de flash al final de la solicitud
        flash.clear()
    except Exception as e:
        flash("Excepción durante la validación: {e}")
        return render_template('formulario.html', formulario=formulario)
        # Limpiar completamente todos los mensajes en la sesión
        session.clear()
        # Limpiar los mens  ajes de flash al final de la solicitud
        flash.clear()

if __name__ == '__main__':
    app.run(debug=True)

import json

def guardar_usuario(usuario):
    usuarios_dir = 'usuarios'
    os.makedirs(usuarios_dir, exist_ok=True)

    # Obtener la lista actual de usuarios
    usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')

    try:
        if os.path.exists(usuarios_file) and os.path.getsize(usuarios_file) > 0:
            with open(usuarios_file, 'r') as file:
                try:
                    usuarios = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Error al cargar usuarios JSON: {e}")
                    usuarios = []  # En caso de error, inicializa como una lista vacía
        else:
            usuarios = []
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")

    # Agregar el nuevo usuario
    usuarios.append(usuario)

    # Guardar la lista actualizada de usuarios
    with open(usuarios_file, 'w') as file:
        json.dump(usuarios, file, indent=2)  # Agregar indent para una mejor legibilidad
