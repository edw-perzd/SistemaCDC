from flask import Blueprint, render_template, redirect, url_for

error_views = Blueprint('error', __name__)

@error_views.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html')

@error_views.app_errorhandler(401)
def unauthorized(error):
    return redirect(url_for('user.login'))