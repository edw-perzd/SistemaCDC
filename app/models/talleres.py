from .db import get_connection


mydb = get_connection()

class Taller():
    def __init__(self, id, nombre, descrip, categoria, fechaRegistro, id_profesor='', fechaAsignacion=None):
        self.id = id
        self.nombre = nombre
        self.descrip = descrip
        self.categoria = categoria
        self.fechaRegistro = fechaRegistro
        self.id_profesor = id_profesor
        self.fechaAsignacion = fechaAsignacion

    def guardar(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO talleres(nombre_taller, descrip_taller, categoria_taller, id_profesor, fechaRegistro_taller) VALUES(%s, %s, %s, %s, %s)"
                val = (self.nombre, self.descrip, self.categoria, self.id_profesor, self.fechaRegistro)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        else:
            with mydb.cursor() as cursor:
                sql = 'UPDATE talleres SET nombre_taller = %s, descrip_taller = %s, categoria_taller = %s, id_profesor = %s, fechaRegistro_taller = %s '
                sql += 'WHERE id_taller = %s'
                val = (self.nombre, self.descrip, self.categoria, self.id_profesor, self.fechaRegistro, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id
            
    def eliminar(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM talleres WHERE id_taller = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
    def asignar(self):
        if self.fechaAsignacion is None:
            with mydb.cursor() as cursor:
                sql = "UPDATE talleres SET id_profesor = %s WHERE id_taller = %s"
                val = (self.id_profesor, self.id_taller)
                cursor.execute(sql, val)
                mydb.commit()
                self.id_taller = cursor.lastrowid
                return self.id_taller
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE talleres SET id_profesor = %s, fechaAsignacion_taller= %s WHERE id_taller = %s"
                val = (self.id_profesor, self.fechaAsignacion, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                self.id_taller = cursor.lastrowid
                return self.id_taller
    def deassign(self):
        with mydb.cursor() as cursor:
            sql = f"UPDATE talleres SET id_profesor = NULL, fechaAsignacion_taller = NULL WHERE id_profesor = { self.id_profesor } AND id_taller = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id_profesor

    @staticmethod
    def validAsign(id_profesor, id_taller):
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM talleres WHERE id_profesor = %s AND id_taller = %s"
            val = (id_profesor, id_taller)
            cursor.execute(sql, val)
            taller = cursor.fetchone()

            if taller:
                valid = Taller(id_taller, taller['nombre_taller'], taller['descrip_taller'], taller['categoria_taller'], taller['fechaRegistro_taller'], id_profesor, taller['fechaAsignacion_taller'])
                return valid
            else:
                return None

    @staticmethod
    def get_tall_by_name(nombre, limit=10, page=1):
        offset = limit * page - limit
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE nombre_taller LIKE '{ nombre }%'; LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for taller in result:
                talleres.append(Taller(id=taller["id_taller"], nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                )
            return talleres

    @staticmethod
    def get_tall_by_cat(cat, limit=10, page=1):
        offset = limit * page - limit
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE categoria_taller LIKE '{ cat }%' LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for taller in result:
                talleres.append(Taller(id=taller["id_taller"], nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                )
            return talleres
        
    @staticmethod
    def __get__(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE id_taller = { id }"
            cursor.execute(sql)

            taller = cursor.fetchone()

            if taller:
                taller = Taller(id, taller["nombre_taller"], taller["descrip_taller"], taller["categoria_taller"], taller["fechaRegistro_taller"], taller["id_profesor"], taller['fechaAsignacion_taller'])
                return taller
            
            return None
        
    @staticmethod
    def get_talleres_by_id(id):
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f'SELECT * FROM talleres WHERE id_profesor = { id }'
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for taller in result:
                    if taller['fechaAsignacion_taller'] != None:
                        talleres.append(Taller(taller['id_taller'], taller['nombre_taller'], taller['descrip_taller'], taller['categoria_taller'], taller['fechaRegistro_taller'], id, taller['fechaAsignacion_taller']))
                return talleres
            else:
                return None

    @staticmethod
    def get_talleres_by_prof(id_profesor, id_taller):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE id_profesor = { id_profesor } AND id_taller = { id_taller }"
            cursor.execute(sql)
            taller = cursor.fetchone()
            if taller:
                tal = Taller(taller['id_taller'], taller['nombre_taller'], ['descrip_taller'], taller['categoria_taller'], taller['fechaRegistro_taller'], id_profesor, taller['fechaAsignacion_taller'])
                return tal
            return None

    @staticmethod
    def get_all(limit=10, page=1):
        offset = limit * page - limit
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for taller in result:
                talleres.append(Taller(id=taller["id_taller"], nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                )
            return talleres
        
    @staticmethod
    def get_all_tal():
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres"
            cursor.execute(sql)
            result = cursor.fetchall()
            for taller in result:
                talleres.append(Taller(id=taller["id_taller"], nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                )
            return talleres

    @staticmethod
    def count_all():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT count(id_taller) as total FROM talleres"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['total']
    
class Asignado:

    def __init__(self, id_taller, nombre_taller, id_profesor, nombre_profesor, aPaterno_profesor, aMaterno_profesor, correoE_profesor, telefono_profesor, edad_profesor, fechaAsignacion='', descrip_taller=''):
        self.id_taller = id_taller
        self.nombre_taller = nombre_taller
        self.id_profesor = id_profesor
        self.nombre_profesor = nombre_profesor
        self.aPaterno_profesor = aPaterno_profesor
        self.aMaterno_profesor = aMaterno_profesor
        self.correoE_profesor = correoE_profesor
        self.telefono_profesor = telefono_profesor
        self.edad_profesor = edad_profesor
        self.fechaAsignacion = fechaAsignacion
        self.descrip_taller = descrip_taller
        
    @staticmethod
    def solicitudes_prof():
        solicitudes = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM talleres WHERE id_profesor IS NOT NULL AND fechaAsignacion_taller IS NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result != None:
                for solicitud in result:
                    sqlp = f"SELECT * FROM profesores WHERE id_profesor = { solicitud['id_profesor'] }"
                    cursor.execute(sqlp)
                    profes = cursor.fetchone()
                    if profes:
                        solicitudes.append(Asignado(solicitud['id_taller'], solicitud['nombre_taller'], solicitud['id_profesor'], profes['nombre_profesor'], profes['aPaterno_profesor'], profes['aMaterno_profesor'], profes['correoE_profesor'], profes['telefono_profesor'], profes['edad_profesor'],))
                return solicitudes
            else:
                return None
    
    @staticmethod
    def solicitar_asign(id_profesor, id_taller):
        with mydb.cursor() as cursor:
            sql = "UPDATE talleres SET id_profesor = %s WHERE id_taller = %s"
            val = (id_profesor, id_taller)
            cursor.execute(sql, val)
            mydb.commit()
            id = cursor.lastrowid
            return id

    @staticmethod
    def verificar_asign(id_taller):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE id_profesor IS NULL AND id_taller = { id_taller }"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return 'Hay espacio para solicitar'
            else:
                return None  

    @staticmethod
    def get_talleres_by_correo(correoE, limit=2, page=1):
        offset = limit * page - limit
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT talleres.*, profesores.* FROM talleres, profesores WHERE profesores.correoE_profesor = '{ correoE }' AND talleres.id_profesor = profesores.id_profesor LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for taller in result:
                    if taller['fechaAsignacion_taller'] != None:
                        talleres.append(Asignado(taller['id_taller'], taller['nombre_taller'], taller['id_profesor'], taller['nombre_profesor'], taller['aPaterno_profesor'], taller['aMaterno_profesor'], taller['correoE_profesor'], taller['telefono_profesor'], taller['edad_profesor'], None, taller['descrip_taller']))
                return talleres
            else:
                return None  
    @staticmethod
    def get_asign_by_correo(correoE):
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT talleres.*, profesores.* FROM talleres, profesores WHERE profesores.correoE_profesor = '{ correoE }' AND talleres.id_profesor = profesores.id_profesor"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for taller in result:
                    if taller['fechaAsignacion_taller'] != None:
                        talleres.append(Asignado(taller['id_taller'], taller['nombre_taller'], taller['id_profesor'], taller['nombre_profesor'], taller['aPaterno_profesor'], taller['aMaterno_profesor'], taller['correoE_profesor'], taller['telefono_profesor'], taller['edad_profesor'], None, taller['descrip_taller']))
                return talleres
            else:
                return None  
                  
    @staticmethod
    def get_talleres_by_fecha(fecha):
        talleres = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT talleres.*, profesores.* FROM talleres, profesores WHERE talleres.fechaAsignacion_taller >= '{ fecha }' AND talleres.id_profesor = profesores.id_profesor"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for taller in result:
                    if taller['fechaAsignacion_taller'] != None:
                        talleres.append(Asignado(taller['id_taller'], taller['nombre_taller'], taller['id_profesor'], taller['nombre_profesor'], taller['aPaterno_profesor'], taller['aMaterno_profesor'], taller['correoE_profesor'], taller['telefono_profesor'], taller['edad_profesor'], taller['fechaAsignacion']))
                return talleres
            else:
                return None    