from flask import render_template, request, flash, session, redirect, url_for
from app import app
from .registro import guardar_usuario
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
import json
import os

class EmailValidator:
    def __call__(self, form, field):
        try:
            v = validate_email(field.data)
        except EmailSyntaxError as e:
            mensaje = f"Correo electrónico no válido: {str(e)}"
            flash(mensaje, 'danger')
            raise ValidationError(mensaje)
        except EmailNotValidError:
            mensaje = "Correo electrónico no válido"
            flash(mensaje, 'danger')
            raise ValidationError(mensaje)

class EdicionFormulario(FlaskForm):
    def __init__(self, usuario, *args, **kwargs):
        super(EdicionFormulario, self).__init__(*args, **kwargs)
        self.usuario = usuario  # Guardar el usuario actual

    email = StringField('Correo Electrónico', validators=[DataRequired(), EmailValidator()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    contrasena = StringField('Contraseña', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=9, message="El teléfono debe tener 9 dígitos")])
    edad = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=0, message="La edad no puede ser negativa")])
    enviar = SubmitField('Guardar Cambios')
    id = HiddenField('ID')

@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    try:
        usuarios_dir = 'usuarios'
        usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')
        
        if os.path.getsize(usuarios_file) > 0:
            with open(usuarios_file, 'r') as file:
                usuarios = json.load(file)
        else:
            usuarios = []

    except Exception as e:
        mensaje = f"Error al cargar usuarios: {e}"
        flash(mensaje, 'danger')
        usuarios = []

    if usuarios:
        usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
        if usuario:
            formulario_edicion = EdicionFormulario(usuario=usuario)

            if request.method == 'POST':
                if formulario_edicion.validate():
                    # Actualizar datos del usuario
                    usuario['email'] = formulario_edicion.email.data
                    usuario['nombre'] = formulario_edicion.nombre.data
                    usuario['apellidos'] = formulario_edicion.apellidos.data
                    usuario['contrasena'] = formulario_edicion.contrasena.data
                    usuario['telefono'] = formulario_edicion.telefono.data
                    usuario['edad'] = formulario_edicion.edad.data
                    guardar_usuario(usuario)
                    mensaje_exito = "Usuario actualizado correctamente."
                    flash(mensaje_exito, 'success')
                    return redirect(url_for('consulta'))
                else:
                    for field, errors in formulario_edicion.errors.items():
                        for error in errors:
                            mensaje_error = f"Error en {field}: {error}"
                            flash(mensaje_error, 'danger')
                    session.pop('error_flash_shown', None)
                    return render_template('editar_usuario.html', formulario_edicion=formulario_edicion, usuario=usuario)
            else:
                return render_template('editar_usuario.html', formulario_edicion=formulario_edicion, usuario=usuario)
        else:
            return render_template('no_usuarios.html')  # Renderiza una plantilla específica para "no existen usuarios"
    else:
        return render_template('no_usuarios.html')  # Renderiza una plantilla específica para "no existen usuarios"
