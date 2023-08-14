from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired

class GenReportA(FlaskForm):
    fecha = DateField('Desde la fecha de inscripción: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Generar reporte de alumnos')
class GenReportP(FlaskForm):
    fecha = DateField('Desde la fecha de asignación: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Generar reporte de profesores')