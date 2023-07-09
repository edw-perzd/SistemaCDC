from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.secret_key = 'B!1weNAt1T^%kvhUI*S^'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cdctexcalac'

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

def get_by_id(db, id):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT id_alumno, correoE_alumno FROM alumnos WHERE id_alumno = '{}'".format(id)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row != None:
            user = Usuario(row[0], row[1], None)
            return user
        else:
            return None
    except Exception as ex:
        raise Exception(ex)

@login_manager_app.user_loader
def load_user(id):
    return get_by_id(db, id)

# Proceso Login
class Usuario(UserMixin):
    def __init__(self, id, correoE, contrasenia):
        self.id = id
        self.correoE = correoE
        self.contrasenia = contrasenia

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

def loginDB(db, user):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT id_alumno, correoE_alumno, contrasenia_alumno FROM alumnos WHERE correoE_alumno = '{}'".format(user.correoE)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row != None:
            user = Usuario(row[0], row[1], row[2])
            return user
        else:
            return None
    except Exception as ex:
        raise Exception(ex)


###################################
@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        user = Usuario(0, request.form['email'], request.form['password']) 
        logged_user = loginDB(db, user)
        if logged_user != None:
            if logged_user.contrasenia:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña Invalida...")
                return render_template('Login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('Login.html')
    else:
        return render_template('Login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/protected")
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados</h1>"
def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)