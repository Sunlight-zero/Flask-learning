import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('email_config.json'):
    with open('email_config.json') as f:
        email_config = json.load(f)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-can-never-guess'
    # sqlalchemy的默认变量，用于取得数据库变量。
    # 默认使用本地的sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # 当你在环境变量中指定DATABASE_URL的变量后，就会使用该设置作为数据库
    # SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 每个页面显示的博文数
    POSTS_PER_PAGE = 3

    # 邮件服务器相关
    ENABLE_SENDING_ERROR_MAILS = email_config['enable_sending_error_mails']
    MAIL_SERVER = email_config['email_api_url']
    MAIL_USE_SSL = email_config['email_use_ssl']
    MAIL_PORT = email_config['email_api_port']
    MAIL_USERNAME = email_config['email_username']
    # 对于163、QQ等邮箱而言，这里的密码不是登录密码而是授权密码
    MAIL_PASSWORD = email_config['email_password']
    ADMINS = email_config['admin_emails']

    # 是否将日志录入文件(Logging to a file)
    ENABLE_LOGGING_TO_FILES = True

    # # 支持的语言种类
    # LANGUAGES = ['zh-cn', 'en']

