from flask import Flask, render_template, redirect, url_for, request, flash
# from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required

from flask_wtf.csrf import CSRFProtect

# Imports from DB
from db.alumnos import Alumno

# Imports from Forms
from forms.alumno_forms import Ingresar

app = Flask(__name__)

app.secret_key = 'B!1weNAt1T^%kvhUI*S^'

csrf = CSRFProtect()

login_manager_app = LoginManager(app)



@login_manager_app.user_loader
def load_user(id):
    return Alumno.obtener_por_id(id)

    # @classmethod
    # def check_password(self, hashed_password, password):
        #return check_password_hash(hashed_password, password)

###################################
@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Ingresar()
    if form.validate_on_submit():
        # alumno = Alumno(None, None, None, form.correoE.data, form.contrasenia.data, None, None, None) 
        logged_user = Alumno.login(form.correoE.data, form.contrasenia.data)
        if logged_user != None:
            if logged_user.contrasenia:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña Invalida...")
                return render_template('Login.html', form=form)
        else:
            flash("Usuario no encontrado...")
            return render_template('Login.html', form=form)
    return render_template('Login.html', form=form)

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