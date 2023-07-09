import mysql.connector

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",  
        user="root",  
        password="", 
        database="cdctexcalac")
    return mydb

def loginDB(db, alumno):
    try:
        cursor = db.cursor()
        sql = "SELECT id_alumno, aPaterno_alumno, aMaterno_alumno FROM alumnos WHERE correoE_alumno=%s AND contrasenia_alumno=%s"
        val= (alumno[0], alumno[1])
        cursor.execute(sql, val)
        row=cursor.fetchone()
        if row != None:
            check = [row[0], row[1], row[2]]
            return check
        else:
            return None
    except Exception as Ex:
        raise Exception(Ex)
