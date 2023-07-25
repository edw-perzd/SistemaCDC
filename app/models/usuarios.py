from .db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

mydb = get_connection()

class Usuario(UserMixin):

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
            if self.rol == '1':
                with mydb.cursor() as cursor:
                    sql = "UPDATE alumnos SET nombre_alumno = %s, aPaterno_alumno = %s, aMaterno_alumno = %s, correoE_alumno = %s, contrasenia_alumno = %s, telefono_alumno = %s, edad_alumno = %d WHERE id_alumno = %s"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.id)
                    cursor.execute(sql, val)
                    mydb.commit()
                    return self.id
            elif self.rol == '2':
                with mydb.cursor() as cursor:
                    sql = "UPDATE profesores SET nombre_profesor = %s, aPaterno_profesor = %s, aMaterno_profesor = %s, correoE_profesor = %s, contrasenia_profesor = %s, telefono_profesor = %s, edad_profesor = %d WHERE id_profesor = %s"
                    val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.id)
                    cursor.execute(sql, val)
                    mydb.commit()
                    return self.id
            
    def eliminar(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM alumnos WHERE id = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
    ####     
    @staticmethod
    def __get__(id, rol):
        with mydb.cursor(dictionary=True) as cursor:
            if rol == 1:
                sql = f"SELECT * FROM alumnos WHERE id_alumno = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    usuario = Usuario(result["nombre_alumno"], result["aPaterno_alumno"], result["aMaterno_alumno"], result["correoE_alumno"], result["contrasenia_alumno"], result["telefono_alumno"], result["edad_alumno"], rol, result["fechaRegistro_alumno"], id)
                    return usuario
            elif rol == 2:
                sql = f"SELECT * FROM profesores WHERE id_profesor = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    usuario = Usuario(result["nombre_profesor"], result["aPaterno_profesor"], result["aMaterno_profesor"], result["correoE_profesor"], result["contrasenia_profesor"], result["telefono_profesor"], result["edad_profesor"], rol, result["fechaRegistro_profesor"], id)
                    return usuario
            elif rol == 3:
                sql = f"SELECT * FROM administradores WHERE id_admin = { id }"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    usuario = Usuario(result["nombre_admin"], result["aPaterno_admin"], result["aMaterno_admin"], result["correoE_admin"], result["contrasenia_admin"], result["telefono_admin"], result["edad_admin"], rol, None, id)
                    return usuario
            return None
        #

    @staticmethod
    def get_all():
        usuarios = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                usuarios.append(Usuario(item["nombre_alumno"], item["aPaterno_alumno"], item["aMaterno_alumno"], item["correoE_alumno"], item["contrasenia_alumno"], item["telefono_alumno"], item["edad_alumno"], None, item["id_alumno"], item["fechaRegistro_alumno"]))
            return usuarios
    
    @staticmethod
    def count_all():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id_alumno) FROM alumnos"
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
                if Usuario.comparePas(user["contrasenia_alumno"], password):
                    return Usuario.__get__(user["id_alumno"], rol)
            else:
                sql = "SELECT id_profesor, correoE_profesor, contrasenia_profesor FROM profesores WHERE correoE_profesor = %s"
                val = (correoE,)
                cursor.execute(sql, val)
                user = cursor.fetchone()
                if user != None:
                    rol = 2
                    if Usuario.comparePas(user["contrasenia_profesor"], password):
                        return Usuario.__get__(user["id_profesor"], rol)
                else:
                    sql = "SELECT id_admin, correoE_admin, contrasenia_admin FROM administradores WHERE correoE_admin = %s"
                    val = (correoE,)
                    cursor.execute(sql, val)
                    user = cursor.fetchone()
                    if user != None:
                        rol = 3 
                        if Usuario.comparePas(user["contrasenia_admin"], password):
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
    def comparePas(contraform, contraserv):
        if contraform == contraserv:
            return True
        else:
            return False
        
    def __str__(self):
        return f"{ self.id } { self.nombre } { self.aPaterno } { self.aMaterno } { self.correoE } { self.telefono } { self.edad } { self.fechaRegistro } { self.rol }"