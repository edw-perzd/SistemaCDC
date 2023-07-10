from flask_login import UserMixin
from .db import get_connection

mydb = get_connection()

class Alumno(UserMixin):

    def __init__(self, nombre, aPaterno, aMaterno, correoE, contrasenia, telefono, edad, fechaRegistro, id=None):
        self.id = id
        self.nombre = nombre
        self.aPaterno = aPaterno
        self.aMaterno = aMaterno
        self.correoE = correoE
        self.contrasenia = contrasenia
        self.telefono = telefono
        self.edad = edad
        self.fechaRegistro = fechaRegistro

    def guardar(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO alumnos(nombre_alumno, aPaterno_alumno, aMaterno_alumno, correoE_alumno, contrasenia_alumno, telefono_alumno, edad_alumno, fechaRegistro_alumno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.fechaRegistro)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE alumnos SET nombre_alumno = %s, aPaterno_alumno = %s, aMaterno_alumno = %s, correoE_alumno = %s, contrasenia_alumno = %s, telefono_alumno = %s, edad_alumno = %d, fechaRegistro_alumno = %s WHERE id_alumno = %s"
                val = (self.nombre, self.aPaterno, self.aMaterno, self.correoE, self.contrasenia, self.telefono, self.edad, self.fechaRegistro, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id
            
    def eliminar(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM alumnos WHERE id = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
            
    @staticmethod
    def obtener_por_id(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos WHERE id_alumno = { id }"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            alumno = Alumno(result["nombre_alumno"], result["aPaterno_alumno"], result["aMaterno_alumno"], result["correoE_alumno"], result["contrasenia_alumno"], result["telefono_alumno"], result["edad_alumno"], result["fechaRegistro_alumno"], id)
            return alumno
        
    @staticmethod
    def get_all():
        alumnos = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM alumnos"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                alumnos.append(Alumno(item["nombre_alumno"], item["aPaterno_alumno"], item["aMaterno_alumno"], item["correoE_alumno"], item["contrasenia_alumno"], item["telefono_alumno"], item["edad_alumno"], item["fechaRegistro_alumno"], item["id_alumno"]))
            return alumnos
    
    @staticmethod
    def count_all():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id_alumno) FROM alumnos"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    @staticmethod
    def login(correoE, contrasenia):
        try:
            with mydb.cursor() as cursor:
                sql = "SELECT id_alumno, correoE_alumno, contrasenia_alumno FROM alumnos WHERE correoE_alumno = '{}'".format(correoE)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    alumno = Alumno(None, None, None, row[1], Alumno.comparePas(contrasenia,row[2]), None, None, None, row[0])
                    return alumno
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
    @staticmethod
    def comparePas(contraform, contraserv):
        if contraform == contraserv:
            return True
        else:
            return False
        
   # def __str__(self):
        #return f"{ self.id } - { self.category }"