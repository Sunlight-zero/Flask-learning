from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.localize_callback
login.login_view = 'login'
mail = Mail(app)

from app import routes, models, localization, errors

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
