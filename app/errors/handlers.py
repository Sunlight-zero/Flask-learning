from flask import render_template
from app import db
from app.errors import bp

# .app_errorhandler 类似于 .errorhandler，不过这里是与 blueprint 关联的
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404error.html'), 404

@bp.app_errorhandler(500)
def internel_error(error):
    db.session.rollback()
    return render_template('errors/500error.html'), 500
