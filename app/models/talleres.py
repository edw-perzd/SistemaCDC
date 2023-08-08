from .db import get_connection

mydb = get_connection()

class Taller():
    def __init__(self, id, nombre, descrip, categoria, id_admin, fechaRegistro, id_profesor=''):
        self.id = id
        self.nombre = nombre
        self.descrip = descrip
        self.categoria = categoria
        self.id_admin = id_admin
        self.fechaRegistro = fechaRegistro
        self.id_profesor = id_profesor

    def guardar(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO talleres(nombre_taller, descrip_taller, categoria_taller, id_admin, id_profesor, fechaRegistro_taller) VALUES(%s, %s, %s, %s, %s, %s)"
                val = (self.nombre, self.descrip, self.categoria, self.id_admin, self.id_profesor, self.fechaRegistro)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        else:
            with mydb.cursor() as cursor:
                sql = 'UPDATE talleres SET nombre_taller = %s, descrip_taller = %s, categoria_taller = %s, id_admin = %s, id_profesor = %s, fechaRegistro_taller = %s '
                sql += 'WHERE id = %s'
                val = (self.nombre, self.descrip, self.categoria, self.id_admin, self.id_profesor, self.fechaRegistro, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id
            
    def eliminar(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM talleres WHERE id_taller = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
        
    @staticmethod
    def __get__(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM talleres WHERE id_taller = { id }"
            cursor.execute(sql)

            taller = cursor.fetchone()

            if taller:
                taller = Taller(id=id, nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_admin=taller["id_admin"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                return taller
            
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
                talleres.append(Taller(id=taller["id_taller"], nombre=taller["nombre_taller"], descrip=taller["descrip_taller"], categoria=taller["categoria_taller"], id_admin=taller["id_admin"], id_profesor=taller["id_profesor"], fechaRegistro=taller["fechaRegistro_taller"])
                )
            return talleres
    @staticmethod
    def count_all():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT count(id_taller) as total FROM talleres"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['total']
    