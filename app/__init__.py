from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.localize_callback
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.users import bp as users_bp
    from app.blogs import bp as blogs_bp
    from app.main import bp as main_bp
    # 将 blueprint 注册到 app 中
    # 此时所有的视图函数、HTML模板、错误处理器(error handlers)
    # 将与 app 关联
    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
    # 使用 url_prefix 参数可以添加前缀，此时应该用 /auth/login.html 访问登录页面
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(blogs_bp, url_prefix='/blogs')

    if app.config['ENABLE_SENDING_ERROR_MAILS']:
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=app.config['ADMINS'],
            subject='PAPERWAREHOUSE SERVER ERROR',
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        )
        # 设置日志的级别为ERROR
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if app.config['ENABLE_LOGGING_TO_FILES']:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/paperwarehouse.log', maxBytes=10240, backupCount=10)
        # setFormatter 可以设置自定义的log格式
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Paperwarehouse start up')
    
    return app


from app import models, localization
