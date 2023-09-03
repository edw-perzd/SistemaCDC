from flask import Blueprint, render_template, abort

from models.talleres import Taller

home_views = Blueprint('home', __name__)

@home_views.route("/")
@home_views.route("/home/")
def home():
    return render_template('home/home.html')

@home_views.route("/home/info_texcalac")
def info_texcalac():
    return render_template('home/infoTexca.html')

@home_views.route("/home/info_talleres")
@home_views.route("/home/info_talleres/<int:page>", methods=['GET'])
def info_talleres(page=1):
    limit = 5
    talleres = Taller.get_all(limit=limit, page=page)
    if talleres is None: abort(404)
    return render_template('home/infotalleres.html', talleres=talleres, page=page)