from flask import render_template, url_for, request
from flask_login import current_user, login_required
from app import app
from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='主页')