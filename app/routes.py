from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sunlight'}
    return render_template('index.html', title='主页', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('正在处理{}的登录请求'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)
