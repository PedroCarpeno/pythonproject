# En el archivo forms.py dentro de la carpeta forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
import json
import os
from app import app
from flask import render_template, request,flash,session,redirect, url_for
#Limite de usuarios
LIMITE_USUARIOS=3

class EmailValidator:
    def __call__(self, form, field):
        try:
            # Intenta validar el correo electrónico
            v = validate_email(field.data)
        except EmailSyntaxError as e:
            mensaje = "Correo electrónico no válido: {}".format(str(e))
            flash(mensaje, 'danger')
            raise ValidationError(mensaje)
        except EmailNotValidError:
            mensaje = "Correo electrónico no válido"
            flash(mensaje, 'danger')
            raise ValidationError(mensaje)


class MiFormulario(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(MiFormulario, self).__init__(*args, **kwargs)
        
        if control_numero_usuarios() >= LIMITE_USUARIOS:
            flash("Limite del fichero ./usuarios/usuarios.jsn alcanzado, no se pueden agregar más usuarios.", 'danger')
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
    id = HiddenField('ID')

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
                    mensaje = "Error al cargar usuarios JSON: {}".format(e)
                    flash(mensaje, 'danger')
    except Exception as e:
        mensaje = "Error al cargar usuarios: {}".format(e)
        flash(mensaje, 'danger')
    return len(usuarios)

def max_id():
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
    return max(usuarios, key=lambda x: x['id'])['id']


@app.route('/procesar_formulario_de_registro', methods=['POST'])
def procesar_formulario_de_registro():
    formularioDeRegistro = MiFormulario(request.form)
    try:
        if formularioDeRegistro.validate():
            # Aquí puedes acceder a los datos del formulario
            nombre = formularioDeRegistro.nombre.data
            email = formularioDeRegistro.email.data
            apellidos = formularioDeRegistro.apellidos.data
            contrasena = formularioDeRegistro.contrasena.data
            telefono = formularioDeRegistro.telefono.data
            edad = formularioDeRegistro.edad.data

            # Construir un diccionario con los datos
            usuario = {
                'id': max_id()+1,
                'nombre': nombre,
                'email': email,
                'apellidos': apellidos,
                'contrasena': contrasena,
                'telefono': telefono,
                'edad':edad
            }
            guardar_usuario(usuario)
            # Puedes hacer algo con los datos, como almacenarlos en una base de datos
            mensaje = "Formulario procesado correctamente."
            flash(mensaje, 'success')
            # Reiniciar el formulario para el próximo usuario
            return redirect(url_for('index'))
        else:
            mensaje = "Error en el formulario. Por favor, verifica los datos."
            flash(mensaje, 'danger')
            session.pop('error_flash_shown', None)
            return render_template('registro.html', formularioDeRegistro=formularioDeRegistro)
    except Exception as e:
       mensaje = "Excepción durante la validación: {}".format(e)
       flash(mensaje, 'danger')
    return render_template('registro.html', formularioDeRegistro=formularioDeRegistro)


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
        usuarios = []
    
    # Buscar el usuario por ID
    usuario_existente = next((u for u in usuarios if u['id'] == usuario['id']), None)

    if usuario_existente:
        # Si el usuario ya existe, actualizar sus campos
        usuario_existente.update(usuario)
    else:
        # Si el usuario no existe, agregarlo a la lista
        usuarios.append(usuario)

    # Guardar la lista actualizada de usuarios
    with open(usuarios_file, 'w') as file:
        json.dump(usuarios, file, indent=2)  # Agregar indent para una mejor legibilidad

@app.route('/registro')
def registro():
    formularioDeRegistro = MiFormulario()
    try:
        usuarios_dir = 'usuarios'
        usuarios_file = os.path.join(usuarios_dir, 'usuarios.json')

        if os.path.getsize(usuarios_file) > 0:
            with open(usuarios_file, 'r') as file:
                usuarios = json.load(file)
        else:
            usuarios = []

    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        usuarios = []

    return render_template('registro.html', formularioDeRegistro=formularioDeRegistro,usuarios=usuarios)