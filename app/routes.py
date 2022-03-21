from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from app import app, db
from app.forms import LoginForm, RegisrationForm, EditProfileForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='主页')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('正在处理{}的登录请求'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/resigter', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，您已成为本网站的会员！')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Happy mathematical analysis!'},
        {'author': user, 'body': 'Fucking real analysis!'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # 检查是否与当前的信息一致，如一致则不做修改
        flag = False
        if current_user.username != form.username.data:
            flag = True
            current_user.username = form.username.data
        if current_user.about_me != form.about_me.data:
            flag = True
            current_user.about_me = form.about_me.data
        if flag:
            db.session.commit()
            flash('您的修改已保存')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='修改个人信息', form=form)
        
