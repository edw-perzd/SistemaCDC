from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

#class Registrarse(FlaskForm):
    #alumno = StringField('Categoría', validators=[DataRequired()])
    #description = StringField('Descripción', validators=[DataRequired()])
    #submit = SubmitField('Guardar')

class Ingresar(FlaskForm):
    correoE = StringField('Correo electrónico', validators=[DataRequired()])
    contrasenia = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Vamos!')