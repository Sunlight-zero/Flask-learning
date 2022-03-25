from app import app
from app.models import User

@app.shell_context_processor
def add_test_users():
    sunlight = User.query.filter_by(username='sunlight').first()
    john = User.query.filter_by(username='john').first()
    return {'sunlight': sunlight, 'john': john}