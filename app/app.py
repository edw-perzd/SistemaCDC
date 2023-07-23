from flask import Flask

from flask_wtf.csrf import CSRFProtect

# Import from Views
from views.home_views import home_views
from views.users_views import user_views
from views.error_views import error_views

app = Flask(__name__)

app.secret_key = 'B!1weNAt1T^%kvhUI*S^'

csrf = CSRFProtect()

app.register_blueprint(home_views)
app.register_blueprint(user_views)
app.register_blueprint(error_views)

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True)