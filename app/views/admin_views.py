from flask import Blueprint, redirect, render_template, url_for, flash, abort, session

from models.usuarios import Usuario,Toma
from models.talleres import Taller

from forms.usuarios_forms import CrearUsuario, ActualizarUsuario

import datetime

admin_views = Blueprint('admin', __name__)

@admin_views.route("/admin/")
def admin():
    if session.get('rol') == 3:
        return render_template('admin/admin.html')
    else:
        abort(404)

@admin_views.route("/admin/alumnos")
@admin_views.route('/admin/alumnos/<int:page>/')
def adminA(page=1):
    if session.get('rol') == 3:
        limit = 5
        alumnos = Usuario.get_all_alm(limit=limit, page=page)
        total_usuarios = Usuario.count_all_alm()
        pages = total_usuarios // limit
        
        talleres = []
        for alumno in alumnos:
            tal = Toma.get_talleres_by_id(alumno.id)
            if tal != None:
                for taller in tal:
                    talleres.append(taller)

        return render_template('admin/adminA.html', alumnos=alumnos, pages=pages, talleres=talleres)
    else:
        abort(401)

@admin_views.route("/admin/profesores")
@admin_views.route('/admin/profesores/<int:page>/')
def adminP(page=1):
    if session.get('rol') == 3:
        limit = 5
        profesores = Usuario.get_all_prof(limit=limit, page=page)
        total_usuarios = Usuario.count_all_prof()
        pages = total_usuarios // limit

        #talleres = Taller.get_all()
        return render_template('admin/adminP.html', profesores=profesores, pages=pages)
    else:
        abort(401)

@admin_views.route("/admin/talleres")
@admin_views.route('/admin/talleres/<int:page>/')
def adminT(page=1):
    if session.get('rol') == 3:
        limit = 3
        talleres = Taller.get_all(limit=limit, page=page)
        total_talleres = Taller.count_all()
        pages = total_talleres // limit

        #talleres = Taller.get_all()
        return render_template('admin/adminT.html', talleres=talleres, pages=pages)
    else:
        abort(401)

@admin_views.route("/admin/solicitudes")
#@admin_views.route('/admin/solicitudes/<int:page>/')
def solicitudes(page=1):
    if session.get('rol') == 3:
        solicitudes = Toma.solicitudes_alm()

        return render_template('admin/adminS.html', solicitudes=solicitudes)
    else:
        abort(401)

@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/delete", methods=['POST', 'GET'])
def denegar_soli(id, tal):
    if session.get('rol') == 3:
        toma = Toma.get(id, tal)
        if toma is None: abort(404)
        toma.eliminar()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)

@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/inscribir", methods=['POST', 'GET'])
def aceptar_soli(id, tal):
    if session.get('rol') == 3:
        toma = Toma.get(id, tal)
        if toma is None: abort(404)

        fecha_actual = datetime.datetime.now().date()
        toma.fechaInscripcion = fecha_actual
        toma.guardar()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)
        
@admin_views.route("/admin/crear_usuario", methods=['GET', 'POST'])
def crear_usuario():
    if session.get('rol') == 3:
        form = CrearUsuario()
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

            usuario = Usuario(nombre, aPaterno, aMaterno, correoE, contrasenia, telefono, edad, rol, None, fecha_actual)
            usuario.guardar()
            return redirect(url_for('admin.admin'))
        return render_template('admin/registerA.html', form=form)
    else:
        abort(401)

@admin_views.route("/admin/<int:id>/<int:rol>/actualizar_usuario", methods=['GET', 'POST'])
def actualizar_usuario(id, rol):
    if session.get('rol') == 3:
        form = ActualizarUsuario()
        usuario = Usuario.__get__(id, rol)
        if not usuario:
            abort(404)
        if form.validate_on_submit():
            usuario.nombre = form.nombre.data
            usuario.aPaterno = form.aPaterno.data
            usuario.aMaterno = form.aMaterno.data
            usuario.correoE = form.correoE.data
            usuario.telefono = form.telefono.data
            usuario.edad = form.edad.data

            usuario.guardar()
            return redirect(url_for('admin.admin'))
        form.nombre.data = usuario.nombre
        form.aPaterno.data = usuario.aPaterno
        form.aMaterno.data = usuario.aMaterno
        form.correoE.data = usuario.correoE
        form.telefono.data = usuario.telefono
        form.edad.data = usuario.edad
        return render_template('admin/updateU.html', form=form, usuario=usuario)
    else:
        abort(401)

@admin_views.route('/admin/<int:id>/<int:rol>/delete/', methods=['POST', 'GET'])
def delete(id, rol):
    if session.get('rol') == 3:
        user = Usuario.__get__(id, rol)
        print(user.id)
        if user is None: abort(404)
        user.eliminar()
        return redirect(url_for('admin.admin'))
    else:
        abort(404)

@admin_views.route('/admin/<int:id>/delete_tal/', methods=['POST'])
def delete_tal(id):
    if session.get('rol') == 3:
        taller = Taller.__get__(id)
        if taller is None: abort(404)
        taller.eliminar()
        return redirect(url_for('admin.admin'))
    else:
        abort(404)