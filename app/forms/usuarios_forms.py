from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, TelField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from models.usuarios import Usuario

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre(s)', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aPaterno = StringField('Apellido paterno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aMaterno = StringField('Apellido materno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email(message='Este campo debe contener un @ y al menos un punto')])
    contrasenia = PasswordField('Crea una contraseña', validators=[DataRequired(), EqualTo('contrasenia_confirm', message="Las contraseñas deben coincidir"), Length(min=8, max=15, message='La contraseña debe contener de 8 a 10 digitos')])
    contrasenia_confirm = PasswordField('Confirma tu contraseña', validators=[DataRequired(), Length(min=8, max=15)])
    telefono = TelField('Número de telefono', validators=[DataRequired(), Length(min=10, max=10, message='El número de teléfono debe contener al menos 10 digitos')])
    edad = IntegerField('Edad', validators=[DataRequired()])
    rol = SelectField('Selecciona tu rol', choices=[('1', 'Alumno'), ('2', 'Profesor')])
    submit = SubmitField('Registrarme')

    def validate_correoE(self, field):
        ######## Consultar si el correo existe en la base de datos ####### 
        if Usuario.check_email(field.data):
            raise ValidationError('El correo ya existe')
    def validate_telefono(self, field):
        ######## Consultar si el telefono existe en la base de datos #######
        if Usuario.check_phone(field.data):
            raise ValidationError('Este número ya existe')


class LoginForm(FlaskForm):
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    contrasenia = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Vamos!')

class CrearUsuario(FlaskForm):
    nombre = StringField('Nombre(s)', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aPaterno = StringField('Apellido paterno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aMaterno = StringField('Apellido materno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email(message='Este campo debe contener un @ y al menos un punto')])
    contrasenia = PasswordField('Contraseña provisional', validators=[DataRequired(), EqualTo('contrasenia_confirm', message="Las contraseñas deben coincidir"), Length(min=8, max=15, message='La contraseña debe contener de 8 a 10 digitos')])
    contrasenia_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(),])
    telefono = TelField('Número de telefono', validators=[DataRequired(), Length(min=10, max=10, message='El número de teléfono debe contener al menos 10 digitos')])
    edad = IntegerField('Edad', validators=[DataRequired()])
    rol = SelectField('Rol de este usuario', choices=[('1', 'Alumno'), ('2', 'Profesor')])
    submit = SubmitField('Registrar')

    def validate_correoE(self, field):
        ######## Consultar si el correo existe en la base de datos #######
        if Usuario.check_email(field.data):
            raise ValidationError('El correo ya existe')
    def validate_telefono(self, field):
        ######## Consultar si el telefono existe en la base de datos #######
        if Usuario.check_phone(field.data):
            raise ValidationError('Este número ya existe')

class ActualizarUsuario(FlaskForm):
    nombre = StringField('Nombre(s)', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aPaterno = StringField('Apellido paterno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    aMaterno = StringField('Apellido materno', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email(message='Este campo debe contener un @ y al menos un punto')])
    telefono = TelField('Número de telefono', validators=[DataRequired(), Length(min=10, max=10, message='El número de teléfono debe contener al menos 10 digitos')])
    edad = IntegerField('Edad', validators=[DataRequired()])
    submit = SubmitField('Guardar')