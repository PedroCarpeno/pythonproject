from app import app
from flask import Flask, render_template, request, jsonify,flash,redirect,url_for
import json
import os
from flask_ngrok import run_with_ngrok
from .registro import guardar_usuario

# Ruta para borrar un usuario
@app.route('/borrar_usuario/<int:usuario_id>')
def borrar_usuario(usuario_id):
    try:
        usuarios_dir = 'usuarios'
        usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')

        if os.path.exists(usuarios_file) and os.path.getsize(usuarios_file) > 0:
            with open(usuarios_file, 'r') as file:
                usuarios = json.load(file)
        else:
            usuarios = []

    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        usuarios = []

    # Buscar el usuario por ID en la lista
    usuario_existente = next((u for u in usuarios if u['id'] == usuario_id), None)

    if usuario_existente:
        # Eliminar el usuario de la lista
        usuarios.remove(usuario_existente)

        # Guardar la lista actualizada de usuarios
        with open(usuarios_file, 'w') as file:
            json.dump(usuarios, file, indent=2)  # Agregar indent para una mejor legibilidad
    else:
        print(f"No se encontró el usuario con ID {usuario_id}")

    return redirect(url_for('consulta'))