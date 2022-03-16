from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sunlight'}
    return render_template('index.html', title='主页', user=user)
