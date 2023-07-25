from flask import Blueprint, redirect, render_template, url_for, flash, abort, session

from models.usuarios import Usuario

from forms.usuarios_forms import LoginForm, RegisterForm

#from utils.file_handler import save_image

import datetime


user_views = Blueprint('user', __name__)

@user_views.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        aPaterno = form.aPaterno.data
        aMaterno = form.aMaterno.data
        correoE = form.correoE.data
        contrasenia = form.contrasenia.data
        telefono = form.telefono.data
        edad = form.edad.data
        rol = form.rol.data
        fecha_actual = datetime.datetime.now().date()

        user = Usuario(nombre, aPaterno, aMaterno, correoE, contrasenia, telefono, edad, rol, None, fecha_actual)
        user.guardar()
        return redirect(url_for('user.login'))
    return render_template('usuarios/register.html', form=form)

@user_views.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correoE = form.correoE.data
        contrasenia = form.contrasenia.data
        user = Usuario.obtener_por_pass(correoE, contrasenia)
        if not user:
            flash('Verifica tus datos')
        else:
            session['id'] = user.id
            session['nombre'] = user.nombre
            session['aPaterno'] = user.aPaterno
            session['aMaterno'] = user.aMaterno
            session['correoE'] = user.correoE
            session['rol'] = user.rol
            return redirect(url_for('home.home'))
    return render_template('usuarios/Login.html', form=form)

@user_views.route("/admin")
def admin():
    if session.get('rol') == 3:
        users = Usuario.get_all()
        return render_template('admin/admin.html', users= users)
    else:
        abort(401)

@user_views.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home.home'))
