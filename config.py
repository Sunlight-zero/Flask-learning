import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-can-never-guess'
    # sqlalchemy的默认变量，用于取得数据库变量。
    # 默认使用本地的sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # 当你在环境变量中指定DATABASE_URL的变量后，就会使用该设置作为数据库
    # SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
