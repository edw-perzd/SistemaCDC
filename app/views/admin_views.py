from flask import Blueprint, redirect, render_template, url_for, flash, abort, session, Response

from models.usuarios import Usuario,Toma
from models.talleres import Taller, Asignado

from io import BytesIO
import math

from forms.usuarios_forms import CrearUsuario, ActualizarUsuario, InscribirAlumnos, DarBajaAlumnos, AsignarTaller, DarBajaProfe, BuscarUsuario

from forms.reportes_forms import GenReportA, GenReportP
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from forms.talleres_forms import CrearTaller, BuscarTaller, ActualizarTaller

import datetime

admin_views = Blueprint('admin', __name__)


@admin_views.route("/admin/", methods=['GET', 'POST'])
@admin_views.route("/admin/alumnos/", methods=['POST', 'GET'])
@admin_views.route('/admin/alumnos/<int:page>/', methods=['GET', 'POST'])
def adminA(page=1):
    if session.get('rol') == 3:
        limit = 5
        total_usuarios = Usuario.count_all_alm()
        pages = math.ceil(total_usuarios / limit)

        form = BuscarUsuario()
        if form.validate_on_submit():
            tipo = form.tipo.data
            texto = form.texto.data   

            if tipo == 1:
                alumnos = Usuario.get_alm_by_name(texto, limit=5)
            elif tipo == 2:
                alumnos = Usuario.get_alm_by_correo(texto, limit=5)
            elif tipo == 3:
                alumnos = Usuario.get_alm_by_tel(texto, limit=5)

            talleres = []
            for alumno in alumnos:
                tal = Toma.get_talleres_by_id(alumno.id)
                if tal != None:
                    for taller in tal:
                        talleres.append(taller)
            return render_template('admin/adminA.html', alumnos=alumnos, talleres=talleres, form=form)

        alumnos = Usuario.get_all_alm(limit=limit, page=page)
        
        talleres = []
        for alumno in alumnos:
            tal = Toma.get_talleres_by_id(alumno.id)
            if tal != None:
                for taller in tal:
                    talleres.append(taller)
        return render_template('admin/adminA.html', alumnos=alumnos, pages=pages, talleres=talleres, form=form)
    else:
        abort(401)

@admin_views.route("/admin/alumnos/<int:id>/inscribir/", methods=['POST', 'GET'])
def inscribir(id):
    if session.get('rol') == 3:
        form = InscribirAlumnos()
        tal = Taller.get_all_tal()
        tf=1
        talleres = [(-1, '')]
        for tall in tal:
            talleres.append((tall.id, tall.nombre))
        form.taller_id.choices = talleres
        user = Usuario.__get__(id, 1)
        if user is None:
            abort(404)

        if form.validate_on_submit():
            taller_id = form.taller_id.data
            if taller_id == -1:
                flash('Selecciona un taller')
            else:
                valid = Toma.validar_inscrip(id, taller_id)
                if valid != None:
                    flash('Este alumno ya esta inscrito o esta en espera de ser inscrito a este taller')
                else:
                    fecha_actual = datetime.datetime.now().date()
                    inscripcion = Toma(id, None, None, None, None, None, None, taller_id, None, None, None, fecha_actual)
                    

                    inscripcion.guardar()
                    return redirect(url_for('admin.adminA'))
        return render_template('admin/inscribir.html', form=form, user=user, tf=tf)
    else:
        abort(404)

@admin_views.route("/admin/alumnos/<int:id>/unsubscribe/", methods=['POST', 'GET'])
def unsubscribe(id):
    if session.get('rol') == 3:
        form = DarBajaAlumnos()
        tal = Toma.get_talleres_by_id(id)

        if tal is None: abort(404)
        tf=2
        talleres = [(-1, '')]
        for tall in tal:
            talleres.append((tall.id_taller, tall.nombre_taller))
        form.taller_id.choices = talleres
        user = Usuario.__get__(id, 1)
        if user is None:
            abort(404)

        if form.validate_on_submit():
            taller_id = form.taller_id.data
            if taller_id == -1:
                flash('Selecciona un taller')
            valid = Toma.get(id, taller_id)
            if valid.fechaInscripcion is None:
                flash('Este alumno esta en espera de inscripcion')
            else:
                valid.eliminar()
                
                return redirect(url_for('admin.adminA'))
        return render_template('admin/inscribir.html', form=form, user=user, tf=tf)
    else:
        abort(404)

@admin_views.route("/admin/profesores/", methods=['POST', 'GET'])
@admin_views.route('/admin/profesores/<int:page>/', methods=['GET', 'POST'])
def adminP(page=1):
    if session.get('rol') == 3:
        limit = 5
        total_usuarios = Usuario.count_all_prof()
        pages = math.ceil(total_usuarios / limit)

        form = BuscarUsuario()
        if form.validate_on_submit():
            tipo = form.tipo.data
            texto = form.texto.data   

            if tipo == 1:
                profesores = Usuario.get_prof_by_name(texto, limit=5)
            elif tipo == 2:
                profesores = Usuario.get_prof_by_correo(texto, limit=5)
            elif tipo == 3:
                profesores = Usuario.get_prof_by_tel(texto, limit=5)

            talleres = []
            for profe in profesores:
                tal = Taller.get_talleres_by_id(profe.id)
                if tal != None:
                    for taller in tal:
                        talleres.append(taller)
            return render_template('admin/adminP.html', profesores=profesores, talleres=talleres, form=form)

        profesores = Usuario.get_all_prof(limit=limit, page=page)

        talleres = []
        for profe in profesores:
            tal = Taller.get_talleres_by_id(profe.id)
            if tal != None:
                for taller in tal:
                    talleres.append(taller)
        
        return render_template('admin/adminP.html', profesores=profesores, pages=pages, talleres=talleres, form=form)
    else:
        abort(401)

@admin_views.route("/admin/profesores/<int:id>/asignar_taller/", methods=['POST', 'GET'])
def asignarT(id):
    if session.get('rol') == 3:
        form = AsignarTaller()
        tal = Taller.get_all_tal()

        tf=1
        talleres = [(-1, '')]
        for tall in tal:
            talleres.append((tall.id, tall.nombre))
        form.taller_id.choices = talleres
        user = Usuario.__get__(id, 2)
        if user is None:
            abort(404)

        if form.validate_on_submit():
            taller_id = form.taller_id.data
            if taller_id == -1:
                flash('Debes seleccionar un taller')
            else:
                valid = Taller.get_talleres_by_prof(id, taller_id)
                if valid != None:
                    flash('Este taller ya esta asignado o el profesor esta en espera de ser asignado a este taller')
                else:
                    fecha_actual = datetime.datetime.now().date()
                    asignar = Taller(taller_id, None, None, None, None, id, fecha_actual)
                    
                    asignar.asignar()
                    return redirect(url_for('admin.adminP'))
        return render_template('admin/inscribir.html', form=form, user=user, tf=tf)
    else:
        abort(404)

@admin_views.route("/admin/profesores/<int:id>/deassign/", methods=['POST', 'GET'])
def deassign(id):
    if session.get('rol') == 3:
        form = DarBajaProfe()
        tal = Taller.get_talleres_by_id(id)

        if tal is None: abort(404)
        tf=2
        talleres = [(-1, '')]
        for tall in tal:
            talleres.append((tall.id, tall.nombre))
        form.taller_id.choices = talleres
        user = Usuario.__get__(id, 2)
        if user is None:
            abort(404)

        if form.validate_on_submit():
            taller_id = form.taller_id.data
            if taller_id == -1:
                flash('Selecciona un taller')
            valid = Taller.get_talleres_by_prof(id, taller_id)
            if valid.fechaAsignacion is None:
                flash('Este profesor esta en espera de asignación')
            else:
                valid.deassign()

                return redirect(url_for('admin.adminA'))
        return render_template('admin/inscribir.html', form=form, user=user, tf=tf)
    else:
        abort(404)

@admin_views.route("/admin/talleres/", methods=['POST', 'GET'])
@admin_views.route('/admin/talleres/<int:page>/', methods=['POST', 'GET'])
def adminT(page=1):
    if session.get('rol') == 3:
        limit = 3
        total_talleres = Taller.count_all()
        pages = math.ceil(total_talleres / limit)

        form = BuscarTaller()
        if form.validate_on_submit():
            tipo = form.tipo.data
            texto = form.texto.data
            if tipo == 1:
                talleres = Taller.get_tall_by_name(texto, limit=5)
            elif tipo == 2:
                talleres = Taller.get_tall_by_cat(texto, limit=5)

            profesores = []
            for profe in profesores:
                tal = Taller.get_talleres_by_id(profe.id)
                if tal != None:
                    for taller in tal:
                        talleres.append(taller)
            return render_template('admin/adminT.html', talleres=talleres, profesores=profesores, form=form)

        talleres = Taller.get_all(limit=limit, page=page)

        profesores = []
        for taller in talleres:
            if taller.id_profesor != None:
                profesores.append(Usuario.__get__(taller.id_profesor, 2))

        return render_template('admin/adminT.html', talleres=talleres, pages=pages, profesores=profesores, form=form)
    else:
        abort(401)

@admin_views.route("/admin/talleres/crear_taller", methods=['POST', 'GET'])
def crearTaller():
    if session.get('rol') == 3:
        form = CrearTaller()
        if form.validate_on_submit():
            nombre = form.nombre.data
            descrip = form.descrip.data
            categoria = form.categoria.data
            
            fecha_actual = datetime.datetime.now().date()

            taller = Taller(None, nombre, descrip, categoria, fecha_actual, None, None)
            taller.guardar()
            return redirect(url_for('admin.adminT'))
        return render_template('admin/crearT.html', form=form)
    else:
        abort(401)

@admin_views.route("/admin/talleres/<int:id>/actualizar_taller/", methods=['GET', 'POST'])
def actualizar_taller(id):
    if session.get('rol') == 3:
        form = ActualizarTaller()
        taller = Taller.__get__(id)
        if not taller:
            abort(404)
        if form.validate_on_submit():
            taller.nombre = form.nombre.data
            taller.descrip = form.descrip.data
            taller.categoria = form.categoria.data

            taller.guardar()
            return redirect(url_for('admin.adminT'))
        form.nombre.data = taller.nombre
        form.descrip.data = taller.descrip
        form.categoria.data = taller.categoria
        return render_template('admin/updateT.html', form=form)
    else:
        abort(401)
        
@admin_views.route('/admin/<int:id>/delete_tal/', methods=['POST'])
def delete_tal(id):
    if session.get('rol') == 3:
        taller = Taller.__get__(id)
        if taller is None: abort(404)
        toma = Toma.get_toma_by_tal(taller.id)
        if toma is None:
            taller.eliminar()
        else:
            flash('Este taller aun tiene alumnos inscritos')
        return redirect(url_for('admin.adminT'))
    else:
        abort(404)

@admin_views.route("/admin/solicitudes/")
def solicitudes():
    if session.get('rol') == 3:
        solicitudes = Toma.solicitudes_alm()

        # Se solicitan las solicitudes de los profesores con un método de la clase Asignado
        soliprof = Asignado.solicitudes_prof()

        return render_template('admin/adminS.html', solicitudes=solicitudes, soliprof=soliprof)
    else:
        abort(401)

@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/delete/", methods=['POST', 'GET'])
def denegar_soli(id, tal):
    if session.get('rol') == 3:
        toma = Toma.get(id, tal)
        if toma is None: abort(404)
        toma.eliminar()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)

@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/inscribir/", methods=['POST', 'GET'])
def aceptar_soli(id, tal):
    if session.get('rol') == 3:
        toma = Toma.get(id, tal)
        if toma is None: abort(404)

        fecha_actual = datetime.datetime.now().date()
        toma.fechaInscripcion = fecha_actual
        toma.inscribir()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)
##
@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/delete_sprof/", methods=['POST', 'GET'])
def denegar_asign(id, tal):
    if session.get('rol') == 3:
        taller = Taller.get_talleres_by_prof(id, tal)
        if taller is None: abort(404)
        taller.deassign()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)

@admin_views.route("/admin/solicitudes/<int:id>/<int:tal>/asignar/", methods=['POST', 'GET'])
def aceptar_asign(id, tal):
    if session.get('rol') == 3:
        taller = Taller.get_talleres_by_prof(id, tal)
        if taller is None: abort(404)

        fecha_actual = datetime.datetime.now().date()
        taller.fechaAsignacion = fecha_actual
        taller.asignar()

        return redirect(url_for('admin.solicitudes'))
    else:
        abort(401)
## 

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
            return redirect(url_for('admin.adminA'))
        return render_template('admin/registerA.html', form=form)
    else:
        abort(401)

@admin_views.route("/admin/<int:id>/<int:rol>/actualizar_usuario/", methods=['GET', 'POST'])
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
            correoE = form.correoE.data
            telefono = form.telefono.data
            usuario.edad = form.edad.data
            
            if correoE == usuario.correoE:
                if telefono == usuario.telefono:
                    usuario.correoE = correoE
                    usuario.telefono = telefono
                    usuario.guardar()
                else:
                    validc = Usuario.check_phone(telefono)
                    if validc is None:
                        usuario.correoE = correoE
                        usuario.telefono = telefono
                        usuario.guardar()
                    else:
                        flash('Este número de teléfono ya existe')
            else:
                validt = Usuario.check_email(correoE)
                if validt is None:
                    if telefono == usuario.telefono:
                        usuario.correoE = correoE
                        usuario.telefono = telefono
                        usuario.guardar()
                    else:
                        validc = Usuario.check_phone(telefono)
                        if validc is None:
                            usuario.correoE = correoE
                            usuario.telefono = telefono
                            usuario.guardar()
                        else:
                            flash('Este número de teléfono ya existe')     
                else:
                    flash('Este correo electrónico ya existe')
                

            return render_template('admin/updateU.html', form=form, usuario=usuario)
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
        if user is None: abort(404)
        user.eliminar()
        return redirect(url_for('admin.adminA'))
    else:
        abort(404)

@admin_views.route('/admin/profile/update_data', methods=['POST', 'GET'])
def update_data():
    if session.get('rol') == 3:
        form = ActualizarUsuario()
        user = Usuario.get_usu_by_correo(session.get('correoE'))
        if not user: abort (404)
        if form.validate_on_submit():
            user.nombre = form.nombre.data
            user.aPaterno = form.aPaterno.data
            user.aMaterno = form.aMaterno.data
            correoE = form.correoE.data
            telefono = form.telefono.data
            user.edad = form.edad.data
            
            if correoE == user.correoE:
                if telefono == user.telefono:
                    user.correoE = correoE
                    user.telefono = telefono
                    user.guardar()
                else:
                    validc = Usuario.check_phone(telefono)
                    if validc is None:
                        user.correoE = correoE
                        user.telefono = telefono
                        user.guardar()
                    else:
                        flash('Este número de teléfono ya existe')
            else:
                validt = Usuario.check_email(correoE)
                if validt is None:
                    if telefono == user.telefono:
                        user.correoE = correoE
                        user.telefono = telefono
                        user.guardar()
                    else:
                        validc = Usuario.check_phone(telefono)
                        if validc is None:
                            user.correoE = correoE
                            user.telefono = telefono
                            user.guardar()
                        else:
                            flash('Este número de teléfono ya existe')     
                else:
                    flash('Este correo electrónico ya existe')
                

            return render_template('admin/update_dataA.html', form=form, user=user)
        form.nombre.data = user.nombre
        form.aPaterno.data = user.aPaterno
        form.aMaterno.data = user.aMaterno
        form.correoE.data = user.correoE
        form.telefono.data = user.telefono
        form.edad.data = user.edad
        return render_template('admin/update_dataA.html', form=form, user=user)
    else:
        abort(404)

@admin_views.route('/admin/reportes/alumnos', methods=['POST', 'GET'])
def reportes():

    form = GenReportA()
    if form.validate_on_submit():
        fecha = form.fecha.data

        # Obtener los talleres por fecha utilizando la función get_talleres_by_fecha
        alumnos_data = Toma.get_talleres_by_fecha(fecha)

        # Crear un objeto PDF en orientación horizontal (landscape)
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

        # Contenido del PDF
        story = []
        styles = getSampleStyleSheet()
        story.append(Paragraph("Reporte de alumnos por fecha", styles['Title']))
        story.append(Paragraph(f"Fecha de inicio: {fecha}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Crear una tabla con los datos de talleres por fecha
        if alumnos_data:
            data = [['ID', 'Nombre(s)', 'Apellido Paterno', 'Apellido Materno', 'Correo Electrónico', 'Teléfono', 'Edad', 'Taller', 'Fecha Inscripción']]
            data.extend([
                [
                    taller.id_alumno,
                    taller.nombre_alumno,
                    taller.aPaterno_alumno,
                    taller.aMaterno_alumno,
                    taller.correoE_alumno,
                    taller.telefono_alumno,
                    taller.edad_alumno,
                    taller.nombre_taller,
                    taller.fechaInscripcion
                ]
                for taller in alumnos_data
            ])

            table = Table(data)
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#cc33b3')),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            story.append(table)
        else:
            story.append(Paragraph("No se encontraron talleres para la fecha especificada.", styles['Normal']))

        # Construir el PDF y guardar en el objeto BytesIO
        doc.build(story)

        # Regresar el archivo PDF como descarga
        pdf_buffer.seek(0)
        return Response(pdf_buffer, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename=reporte_alumnos.pdf'})

    return render_template('admin/reportes.html', form=form)

@admin_views.route('/admin/reportes/profesores', methods=['POST', 'GET'])
def reportesP():
    ##Proceso para reportes de profesores
    form = GenReportP()
    if form.validate_on_submit():
        fecha = form.fecha.data

        # Obtener los talleres por fecha utilizando la función get_talleres_by_fecha
        profes_data = Asignado.get_talleres_by_fecha(fecha)

        # Crear un objeto PDF en orientación horizontal (landscape)
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

        # Contenido del PDF
        story = []
        styles = getSampleStyleSheet()
        story.append(Paragraph("Reporte de profesores por fecha", styles['Title']))
        story.append(Paragraph(f"Fecha de inicio: {fecha}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Crear una tabla con los datos de talleres por fecha
        if profes_data:
            data = [['ID', 'Nombre(s)', 'Apellido Paterno', 'Apellido Materno', 'Correo Electrónico', 'Teléfono', 'Edad', 'Taller a cargo', 'Fecha Inscripción']]
            data.extend([
                [
                    taller.id_profesor,
                    taller.nombre_profesor,
                    taller.aPaterno_profesor,
                    taller.aMaterno_profesor,
                    taller.correoE_profesor,
                    taller.telefono_profesor,
                    taller.edad_profesor,
                    taller.nombre_taller,
                    taller.fechaAsignacion
                ]
                for taller in profes_data
            ])

            table = Table(data)
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#cc33b3')),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            story.append(table)
        else:
            story.append(Paragraph("No se encontraron talleres para la fecha especificada.", styles['Normal']))

        # Construir el PDF y guardar en el objeto BytesIO
        doc.build(story)

        # Regresar el archivo PDF como descarga
        pdf_buffer.seek(0)
        return Response(pdf_buffer, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename=reporte_profesores.pdf'})
    return render_template('admin/reportesP.html', form=form)