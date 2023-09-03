from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

from models.usuarios import Usuario
from models.talleres import Taller

class CrearTaller(FlaskForm):
    nombre = StringField('Nombre del taller', validators=[DataRequired(), Length(min=3, message='Este campo debe contener al menos 3 letras')])
    descrip = TextAreaField('Descripción del taller', validators=[DataRequired(), Length(min=3, message='Este campo debe contener al menos 3 letras')])
    categoria = StringField('Categoria del taller', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    submit = SubmitField('Crear Taller')

class ActualizarTaller(FlaskForm):
    nombre = StringField('Nombre del taller', validators=[DataRequired(), Length(min=3, message='Este campo debe contener al menos 3 letras')])
    descrip = TextAreaField('Descripción del taller', validators=[DataRequired(), Length(min=3, message='Este campo debe contener al menos 3 letras')])
    categoria = StringField('Categoria del taller', validators=[DataRequired(), Length(min=3, max=30, message='Este campo debe contener al menos 3 letras')])
    submit = SubmitField('Guardar Taller')

class BuscarTaller(FlaskForm):
    tipo = SelectField('Buscar por...', coerce=int, choices=[(1, 'Nombre'), (2, 'Categoria')])
    texto = StringField('Busqueda:', validators=[DataRequired(), Length(min=3, message='Este campo debe contener al menos 3 caracteres')])
    submit = SubmitField('Buscar')