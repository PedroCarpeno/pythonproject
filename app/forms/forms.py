# En el archivo forms.py dentro de la carpeta forms
from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
import json
import os

class EmailValidator:
    def __call__(self, form, field):
        try:
            # Intenta validar el correo electrónico
            v = validate_email(field.data)
        except EmailSyntaxError as e:
            flash(f"Correo electrónico no válido: {str(e)}", 'danger')
            raise ValidationError(f"Correo electrónico no válido: {str(e)}")
        except EmailNotValidError:
            flash("Correo electrónico no válido", 'danger')
            raise ValidationError("Correo electrónico no válido")

def control_numero_usuarios():
    usuarios = []
    usuarios_dir = 'usuarios'
    usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')

    try:
        if os.path.exists(usuarios_file):
            with open(usuarios_file, 'r') as file:
                try:
                    usuarios = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Error al cargar usuarios JSON: {e}")
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
    return len(usuarios)


class MiFormulario(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(MiFormulario, self).__init__(*args, **kwargs)
        
        if control_numero_usuarios() >= 2:
            flash("No se pueden agregar más usuarios.", 'danger')
            # Deshabilitar los campos si se supera el límite de usuarios
            self.nombre.render_kw = {'readonly': True}
            self.email.render_kw = {'readonly': True}
            self.apellidos.render_kw = {'readonly': True}
            self.contrasena.render_kw = {'readonly': True}
            self.telefono.render_kw = {'readonly': True}
            self.edad.render_kw = {'readonly': True}
            self.enviar.render_kw = {'disabled': True}

    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), EmailValidator()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    contrasena = StringField('Contraseña', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=9, message="El teléfono debe tener 9 dígitos")])
    edad = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=0, message="La edad no puede ser negativa")])
    enviar = SubmitField('Enviar')

