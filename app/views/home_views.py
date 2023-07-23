from flask import Blueprint, render_template

home_views = Blueprint('home', __name__)

@home_views.route("/")
@home_views.route("/home/")
def home():
    return render_template('home/home.html')