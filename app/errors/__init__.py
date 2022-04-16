from flask import Blueprint

bp = Blueprint('errors', __name__)

# 导入的对象会注册在bp之下
from app.errors import handlers