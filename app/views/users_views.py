from flask import Blueprint, redirect, render_template, url_for, flash, abort, session

from models.usuarios import Usuario, Toma

from models.talleres import Taller, Asignado

from forms.usuarios_forms import LoginForm, RegisterForm, ElegirTaller, OlvideContra, ProfileForm

#from utils.file_handler import save_image

import datetime


user_views = Blueprint('user', __name__)

@user_views.route("/register/", methods=['GET', 'POST'])
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

@user_views.route("/login/", methods=['GET', 'POST'])
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

@user_views.route("/home/mytaller/")
def mytaller():
    if session.get('rol') != 3:
        if session.get('rol') == 1:
            correoE = session.get('correoE')
            talleres = Toma.get_talleres_by_correo(correoE)

            return render_template('usuarios/talleres.html', talleres=talleres)
        elif session.get('rol') == 2:
            talleres = Asignado.get_talleres_by_correo(session.get('correoE'))
            return render_template('usuarios/talleres.html', talleres=talleres)
        else:
            abort(401)
    else:
        abort(401)

@user_views.route("/home/mytaller/solicitar_taller/", methods=['POST', 'GET'])
def validinfo():
    if session.get('rol') != 3:
        if session.get('rol') == 2 or session.get('rol') == 1:
            form = ElegirTaller()
            tal = Taller.get_all_tal()

            talleres = [(-1, '')]
            for tall in tal:
                talleres.append((tall.id, tall.nombre))
            form.taller_id.choices = talleres
            if form.validate_on_submit():
                correoE = form.correoE.data
                taller_id = form.taller_id.data
                contrasenia = form.contrasenia.data
                if taller_id == -1:
                    flash('Debes seleccionar un taller')
                else:
                    if correoE == session.get('correoE'):
                        user = Usuario.obtener_por_pass(correoE, contrasenia)
                        if user:
                            tal = Toma.validar_inscrip(user.id, taller_id)
                            if tal is None:
                                Toma.solicitar_taller(user.id, taller_id)
                                flash('Solicitud enviada al administrador')
                            else:
                                flash('Ya estas inscrito en este taller o ya lo solicitaste anteriormente')
                        else:
                            flash('Contraseña incorrecta')
                    else:
                        flash('Verifica tu correo electrónico')

            return render_template('usuarios/validform.html', form=form)
        else:
            abort(401)
    else:
        abort(401)

@user_views.route("/home/mytaller/solicitar_impartir/", methods=['POST', 'GET'])
def solicitar_impartir():
    if session.get('rol') != 3:
        if session.get('rol') == 2 or session.get('rol') == 1:
            form = ElegirTaller()
            tal = Taller.get_all_tal()

            talleres = [(-1, '')]
            for tall in tal:
                talleres.append((tall.id, tall.nombre))
            form.taller_id.choices = talleres
            if form.validate_on_submit():
                correoE = form.correoE.data
                taller_id = form.taller_id.data
                contrasenia = form.contrasenia.data
                if taller_id == -1:
                    flash('Debes seleccionar un taller')
                else:
                    if correoE == session.get('correoE'):
                        user = Usuario.obtener_por_pass(correoE, contrasenia)
                        if user:
                            tal = Taller.get_talleres_by_prof(user.id, taller_id)
                            valid = Asignado.verificar_asign(taller_id)
                            if tal is None:
                                if valid != None:
                                    Asignado.solicitar_asign(user.id, taller_id)
                                    flash('Solicitud enviada al administrador')
                                else:
                                    flash('Este taller ya ha sido solicitado o ya esta ocupado. Consultalo con el administrador')
                            else:
                                flash('Ya estas inscrito en este taller o ya lo solicitaste anteriormente')
                        else:
                            flash('Contraseña incorrecta')
                    else:
                        flash('Verifica tu correo electrónico')

            return render_template('usuarios/validform.html', form=form)
        else:
            abort(401)
    else:
        abort(401)

@user_views.route("/home/olvide_contraseña/", methods=['POST', 'GET'])
def olvidcontra():
    form = OlvideContra()

    if form.validate_on_submit():
        nombre = form.nombre.data
        aPaterno = form.aPaterno.data
        aMaterno = form.aMaterno.data
        correoE = form.correoE.data
        telefono = form.telefono.data
        contrasenia = form.contrasenia.data

        user = Usuario.olvidcontra(nombre, aPaterno, aMaterno, correoE, telefono)
        if user is None:
            flash('Datos erroneos')
        else:
            user.contrasenia = contrasenia
            user.cambio_c()

            return redirect(url_for('user.login'))

    return render_template('usuarios/olvidecontra.html', form=form)

@user_views.route("/home/mi_perfil/", methods=['POST', 'GET'])
def my_profile():
    if session.get('id'):
        form = ProfileForm()
        user = Usuario.get_usu_by_correo(session.get('correoE'))

        if form.validate_on_submit():
            contrasenia = form.contrasenia.data 
            user.contrasenia = contrasenia
            user.cambio_c()
            flash('Se cambio tu contraseña')

        return render_template('usuarios/profile.html', form=form, user=user)
    else:
        abort(404)


@user_views.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('home.home'))
