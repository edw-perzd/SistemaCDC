from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre(s)', validators=[DataRequired()])
    aPaterno = StringField('Apellido paterno', validators=[DataRequired()])
    aMaterno = StringField('Apellido materno', validators=[DataRequired()])
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    contrasenia = PasswordField('Crea una contraseña', validators=[DataRequired(), EqualTo('contrasenia_confirm', message="Las contraseñas deben coincidir")])
    contrasenia_confirm = PasswordField('Confirma tu contraseña', validators=[DataRequired(),])
    telefono = StringField('Número de telefono', validators=[DataRequired()])
    edad = IntegerField('Edad', validators=[DataRequired()])
    submit = SubmitField('Registrarme')

class LoginForm(FlaskForm):
    correoE = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    contrasenia = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Vamos!')