from .db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

from models.talleres import Taller

mydb = get_connection()

class Usuario():

    def __init__(self, nombre, aPaterno, aMaterno, correoE, contrasenia, telefono, edad, rol='', id=None, fechaRegistro=''):
        self.id = id
        self.nombre = nombre
        self.aPaterno = aPaterno
        self.aMaterno = aMaterno
        self.correoE = correoE
        self.contrasenia = contrasenia
        self.telefono = telefono
        self.edad = edad
        self.fechaRegistro = fechaRegistro
        self.rol = rol

    def guardar(self):
        # Create a New Object in DB
        if self.id is None:
            self.contrasenia = generate_password_hash(self.contrasenia)
            if self.rol == '1':
                with mydb.cursor() as cursor:
                    sql = "INSERT INTO alumnos(nombre_alumno, aPaterno_alumno, aMaterno_alumno, correoE_alumno, contrasenia_alumno, telefono_alumno, edad_alumno, fechaRegistro_alumno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.fechaRegistro)
                    cursor.execute(sql, val)
                    mydb.commit()
                    self.id = cursor.lastrowid
                    return self.id
            elif self.rol == '2':
                with mydb.cursor() as cursor:
                    sql = "INSERT INTO profesores(nombre_profesor, aPaterno_profesor, aMaterno_profesor, correoE_profesor, contrasenia_profesor, telefono_profesor, edad_profesor, fechaRegistro_profesor) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.fechaRegistro)
                    cursor.execute(sql, val)
                    mydb.commit()
                    self.id = cursor.lastrowid
                    return self.id
        # Update an Object
        else:
            if self.rol == '1' or self.rol == 1:
                with mydb.cursor() as cursor:
                    sql = "UPDATE alumnos SET nombre_alumno = %s, aPaterno_alumno = %s, aMaterno_alumno = %s, correoE_alumno = %s, telefono_alumno = %s, edad_alumno = %s WHERE id_alumno = %s"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.telefono, self.edad, self.id)
                    cursor.execute(sql, val)
                    mydb.commit()
                    return self.id
            elif self.rol == '2' or self.rol == 2:
                with mydb.cursor() as cursor:
                    sql = "UPDATE profesores SET nombre_profesor = %s, aPaterno_profesor = %s, aMaterno_profesor = %s, correoE_profesor = %s, telefono_profesor = %s, edad_profesor = %s WHERE id_profesor = %s"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.telefono, self.edad, self.id)
                    cursor.execute(sql, val)
                    mydb.commit()
                    return self.id
            
    def eliminar(self):
        with mydb.cursor() as cursor:
            if self.rol == '1' or self.rol == 1:
                sql = f"DELETE FROM alumnos WHERE id_alumno = { self.id }"
                cursor.execute(sql)
                mydb.commit()
                return self.id
            elif self.rol == '2' or self.rol == 2:
                sql = f"DELETE FROM profesores WHERE id_profesor = { self.id }"
                cursor.execute(sql)
                mydb.commit()
                return self.id
     
    @staticmethod
    def __get__(id, rol):
        with mydb.cursor(dictionary=True) as cursor:
            if rol == 1:
                sql = f"SELECT * FROM alumnos WHERE id_alumno = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    usuario = Usuario(result["nombre_alumno"], result["aPaterno_alumno"], result["aMaterno_alumno"], result["correoE_alumno"], result["contrasenia_alumno"], result["telefono_alumno"], result["edad_alumno"], rol, id, result["fechaRegistro_alumno"])
                    return usuario
            elif rol == 2:
                sql = f"SELECT * FROM profesores WHERE id_profesor = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    usuario = Usuario(result["nombre_profesor"], result["aPaterno_profesor"], result["aMaterno_profesor"], result["correoE_profesor"], result["contrasenia_profesor"], result["telefono_profesor"], result["edad_profesor"], rol, id, result['fechaRegistro_profesor'])
                    return usuario
            elif rol == 3:
                sql = f"SELECT * FROM administradores WHERE id_admin = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    usuario = Usuario(result["nombre_admin"], result["aPaterno_admin"], result["aMaterno_admin"], result["correoE_admin"], result["contrasenia_admin"], result["telefono_admin"], result["edad_admin"], rol, id, None)
                    return usuario
            return None

    @staticmethod
    def get_all_alm(limit=10, page=1):
        offset = limit * page - limit
        alumnos = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                alumnos.append(Usuario(nombre=item["nombre_alumno"], aPaterno=item["aPaterno_alumno"], aMaterno=item["aMaterno_alumno"], correoE=item["correoE_alumno"], contrasenia=item["contrasenia_alumno"], telefono=item["telefono_alumno"], edad=item["edad_alumno"], rol=1, id=item["id_alumno"], fechaRegistro=item["fechaRegistro_alumno"]))
            return alumnos

    @staticmethod
    def get_all_prof(limit=10, page=1):
        offset = limit * page - limit
        profesores = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM profesores LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                profesores.append(Usuario(item["nombre_profesor"], item["aPaterno_profesor"], item["aMaterno_profesor"], item["correoE_profesor"], item["contrasenia_profesor"], item["telefono_profesor"], item["edad_profesor"], 2, item["id_profesor"], item["fechaRegistro_profesor"]))
            return profesores

    @staticmethod
    def get_prof_by_name(nombre, limit=10, page=1):
        offset = limit * page - limit
        profes = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM profesores WHERE nombre_profesor LIKE '{ nombre }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                profes.append(Usuario(item["nombre_profesor"], item["aPaterno_profesor"], item["aMaterno_profesor"], item["correoE_profesor"], None, item["telefono_profesor"], item["edad_profesor"], 2, item["id_profesor"], item["fechaRegistro_profesor"]))
            return profes

    @staticmethod
    def get_alm_by_name(nombre, limit=10, page=1):
        offset = limit * page - limit
        alumnos = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE nombre_alumno LIKE '{ nombre }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                alumnos.append(Usuario(item["nombre_alumno"], item["aPaterno_alumno"], item["aMaterno_alumno"], item["correoE_alumno"], None, item["telefono_alumno"], item["edad_alumno"], 1, item["id_alumno"], item["fechaRegistro_alumno"]))
            return alumnos

    @staticmethod
    def get_prof_by_correo(correoE, limit=10, page=1):
        profes = []
        offset = limit * page - limit
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM profesores WHERE correoE_profesor LIKE '{ correoE }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                profes.append(Usuario(item["nombre_profesor"], item["aPaterno_profesor"], item["aMaterno_profesor"], item["correoE_profesor"], None, item["telefono_profesor"], item["edad_profesor"], 2, item["id_profesor"], item["fechaRegistro_profesor"]))
            return profes

    @staticmethod
    def get_alm_by_correo(correoE, limit=10, page=1):
        offset = limit * page - limit
        alumnos = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE correoE_alumno LIKE '{ correoE }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                alumnos.append(Usuario(item["nombre_alumno"], item["aPaterno_alumno"], item["aMaterno_alumno"], item["correoE_alumno"], None, item["telefono_alumno"], item["edad_alumno"], 1, item["id_alumno"], item["fechaRegistro_alumno"]))
            return alumnos
        
    @staticmethod
    def get_prof_by_tel(tel, limit=10, page=1):
        offset = limit * page - limit
        profes = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM profesores WHERE telefono_profesor LIKE '{ tel }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                profes.append(Usuario(item["nombre_profesor"], item["aPaterno_profesor"], item["aMaterno_profesor"], item["correoE_profesor"], None, item["telefono_profesor"], item["edad_profesor"], 2, item["id_profesor"], item["fechaRegistro_profesor"]))
            return profes

    @staticmethod
    def get_alm_by_tel(tel, limit=10, page=1):
        offset = limit * page - limit
        alumnos = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE telefono_alumno LIKE '{ tel }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                alumnos.append(Usuario(item["nombre_alumno"], item["aPaterno_alumno"], item["aMaterno_alumno"], item["correoE_alumno"], None, item["telefono_alumno"], item["edad_alumno"], 1, item["id_alumno"], item["fechaRegistro_alumno"]))
            return alumnos

    @staticmethod
    def get_all_admin():
        admins = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM administradores"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                admins.append(Usuario(item["nombre_admin"], item["aPaterno_admin"], item["aMaterno_admin"], item["correoE_admin"], item["contrasenia_admin"], item["telefono_admin"], item["edad_admin"], 3, item["id_admin"], None))
            return admins
    
    @staticmethod
    def count_all_alm():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id_alumno) FROM alumnos"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    @staticmethod
    def count_all_prof():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id_profesor) FROM profesores"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    
    ######
    @staticmethod
    def obtener_por_pass(correoE, password):
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT id_alumno, correoE_alumno, contrasenia_alumno FROM alumnos WHERE correoE_alumno = %s"
            val = (correoE,)
            cursor.execute(sql, val)
            user = cursor.fetchone()
            if user != None:
                rol = 1
                if check_password_hash(user['contrasenia_alumno'], password):
                    return Usuario.__get__(user["id_alumno"], rol)
            else:
                sql = "SELECT id_profesor, correoE_profesor, contrasenia_profesor FROM profesores WHERE correoE_profesor = %s"
                val = (correoE,)
                cursor.execute(sql, val)
                user = cursor.fetchone()
                if user != None:
                    rol = 2
                    if check_password_hash(user['contrasenia_profesor'], password):
                        return Usuario.__get__(user["id_profesor"], rol)
                else:
                    sql = "SELECT id_admin, correoE_admin, contrasenia_admin FROM administradores WHERE correoE_admin = %s"
                    val = (correoE,)
                    cursor.execute(sql, val)
                    user = cursor.fetchone()
                    if user != None:
                        rol = 3 
                        if check_password_hash(user['contrasenia_admin'], password):
                            return Usuario.__get__(user["id_admin"], rol)
                    return None

    @staticmethod
    def obtener_correo(correoE):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE correoE_alumno = { correoE }"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            if result:
                usuario = Usuario(result["nombre_alumno"], result["aPaterno_alumno"], result["aMaterno_alumno"], result["correoE_alumno"], result["contrasenia_alumno"], result["telefono_alumno"], result["edad_alumno"], None, result["fechaRegistro_alumno"], result["id_alumno"])
                return usuario
    
    @staticmethod
    def check_email(correoE):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE correoE_alumno = '{ correoE }'"
            cursor.execute(sql)

            usuario = cursor.fetchone()

            if usuario:
                return 'El correo existe'
            else:
                sql = f"SELECT * FROM profesores WHERE correoE_profesor = '{ correoE }'"
                cursor.execute(sql)

                usuario = cursor.fetchone()

                if usuario:
                    return 'El correo existe'
                else:
                    sql = f"SELECT * FROM administradores WHERE correoE_admin = '{ correoE }'"
                    cursor.execute(sql)

                    usuario = cursor.fetchone()

                    if usuario:
                        return 'El correo existe'
                    else:
                        return None
                    
    @staticmethod
    def check_phone(telefono):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE telefono_alumno = '{ telefono }'"
            cursor.execute(sql)

            usuario = cursor.fetchone()

            if usuario:
                return 'El telefono existe'
            else:
                sql = f"SELECT * FROM profesores WHERE telefono_profesor = '{ telefono }'"
                cursor.execute(sql)

                usuario = cursor.fetchone()

                if usuario:
                    return 'El telefono existe'
                else:
                    sql = f"SELECT * FROM administradores WHERE telefono_admin = '{ telefono }'"
                    cursor.execute(sql)

                    usuario = cursor.fetchone()

                    if usuario:
                        return 'El telefono existe'
                    else:
                        return None     

class Toma:

    def __init__(self, id_alumno, nombre_alumno, aPaterno_alumno, aMaterno_alumno, correoE_alumno, telefono_alumno, edad_alumno, id_taller, nombre_taller, descrip_taller, categoria_taller, fechaInscripcion=''):
        self.id_alumno = id_alumno
        self.nombre_alumno = nombre_alumno
        self.aPaterno_alumno = aPaterno_alumno
        self.aMaterno_alumno = aMaterno_alumno
        self.correoE_alumno = correoE_alumno
        self.telefono_alumno = telefono_alumno
        self.edad_alumno = edad_alumno
        self.id_taller = id_taller
        self.nombre_taller = nombre_taller
        self.descrip_taller = descrip_taller
        self.categoria_taller = categoria_taller
        self.fechaInscripcion = fechaInscripcion

    def guardar(self):
        if self.fechaInscripcion is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO toma(id_alumno, id_taller) "
                sql += "VALUES(%s, %s)"
                val = (self.id_alumno, self.id_taller)
                cursor.execute(sql, val)
                mydb.commit()
                self.id_alumno = cursor.lastrowid
                return self.id_alumno
        else:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO toma(id_alumno, id_taller, fechaInscripcion) "
                sql += "VALUES(%s, %s, %s)"
                val = (self.id_alumno, self.id_taller, self.fechaInscripcion)
                cursor.execute(sql, val)
                mydb.commit()
                self.id_alumno = cursor.lastrowid
                return self.id_alumno

    def inscribir(self):
        with mydb.cursor() as cursor:
                sql = "UPDATE toma SET fechaInscripcion = %s WHERE id_alumno = %s AND id_taller = %s"
                val = (self.fechaInscripcion, self.id_alumno, self.id_taller)
                cursor.execute(sql, val)
                mydb.commit()
                self.id_alumno = cursor.lastrowid
                return self.id_alumno
            

    def eliminar(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM toma WHERE id_alumno = { self.id_alumno } AND id_taller = { self.id_taller }"
            cursor.execute(sql)
            mydb.commit()
            return self.id_alumno
    
    @staticmethod
    def validar_inscrip(id_alumno, id_taller):
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM toma WHERE id_alumno = %s AND id_taller = %s"
            val = (id_alumno, id_taller)
            cursor.execute(sql, val)
            inscrip = cursor.fetchone()

            if inscrip:
                return 'Ya esta inscrito'
            else:
                return None

    @staticmethod
    def get_talleres_by_correo(correoE):
        toma = []
        with mydb.cursor(dictionary=True) as cursor:
            csql = f"SELECT id_alumno FROM alumnos WHERE correoE_alumno = '{ correoE }'"
            cursor.execute(csql)
            result = cursor.fetchone()
            if result:
                id = result['id_alumno']
                sql = f'SELECT toma.*, talleres.*, alumnos.* FROM toma, talleres, alumnos WHERE toma.id_alumno = { id } AND toma.id_taller = talleres.id_taller AND toma.id_alumno = alumnos.id_alumno'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    for taller in result:
                        toma.append(Toma(taller['id_alumno'], taller['nombre_alumno'], taller['aPaterno_alumno'], taller['aMaterno_alumno'], taller['correoE_alumno'], taller['telefono_alumno'], taller['edad_alumno'], taller['id_taller'], taller['nombre_taller'], taller['descrip_taller'], taller['categoria_taller'], taller['fechaInscripcion']))
                    return toma
            else:
                csql = f"SELECT id_profesor FROM profesores WHERE correoE_profesor = { correoE }"
                cursor.execute(csql)
                result = cursor.fetchone()
                if result:
                    id = result['id_profesor']
                    sql = f'SELECT * FROM talleres WHERE id_profesor = { id }'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for taller in result:
                        toma.append(id_profesor=taller['id_profesor'], id_taller=taller['id_taller'], nombre_taller=taller['nombre_taller'], descrip_taller=taller['descrip_taller'])
                    return toma

    @staticmethod
    def get_talleres_by_id(id):
        toma = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f'SELECT toma.*, talleres.* FROM toma, talleres WHERE toma.id_alumno = { id } AND toma.id_taller = talleres.id_taller'
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for taller in result:
                    if taller['fechaInscripcion'] != None:
                        toma.append(Toma(taller['id_alumno'], None, None, None, None, None, None, taller['id_taller'], taller['nombre_taller'], taller['descrip_taller'], taller['categoria_taller'], taller['fechaInscripcion']))
                return toma
            else:
                return None
                
    @staticmethod
    def get(id, tal):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM toma WHERE id_alumno = { id } AND id_taller = { tal }"
            cursor.execute(sql)
            toma = cursor.fetchone()
            if toma:
                toma = Toma(id, None, None, None, None, None, None, toma['id_taller'], None, None, None, toma['fechaInscripcion'])
                return toma
            return None

    @staticmethod
    def get_toma_by_tal(id_taller):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM toma WHERE id_taller = { id_taller }"
            cursor.execute(sql)

            taller = cursor.fetchone()

            if taller:
                taller = Toma(taller['id_alumno'], None, None, None, None, None, None, taller['id_taller'], None, None, None, taller['fechaInscripcion'])
                return taller
            
            return None
        
    @staticmethod
    def solicitudes_alm():
        solicitudes = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM toma WHERE fechaInscripcion is null"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result != None:
                for solicitud in result:
                    alumnos = Usuario.__get__(solicitud['id_alumno'], 1)
                    talleres = Taller.__get__(solicitud['id_taller'])
                    solicitudes.append(Toma(solicitud['id_alumno'], alumnos.nombre, alumnos.aPaterno, alumnos.aMaterno, alumnos.correoE, alumnos.telefono, alumnos.edad, solicitud['id_taller'], talleres.nombre, talleres.descrip, talleres.categoria, None))
                return solicitudes
            else:
                return None
            

    def __str__(self):
        return f"{ self.id } { self.nombre } { self.aPaterno } { self.aMaterno } { self.correoE } { self.telefono } { self.edad } { self.fechaRegistro } { self.rol }"