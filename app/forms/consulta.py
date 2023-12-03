from app import app
from flask import Flask, render_template, request, jsonify,flash,redirect,url_for
import json
import os
from flask_ngrok import run_with_ngrok

@app.route('/consulta')
def consulta():
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

    return render_template('consulta.html', usuarios=usuarios)