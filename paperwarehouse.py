from app import create_app, db
from app.models import User, Post

app = create_app()

# 添加flask shell上下文变量，使用修饰器让它在flask shell初始化时自动引入：
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

from test_users import add_test_users
