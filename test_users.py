from paperwarehouse import app
# from flask import current_app
from app.models import User

# flask 里的 current_app 是上下文相关的
@app.shell_context_processor
def add_test_users():
    sunlight = User.query.filter_by(username='sunlight').first()
    john = User.query.filter_by(username='john').first()
    return {'sunlight': sunlight, 'john': john}