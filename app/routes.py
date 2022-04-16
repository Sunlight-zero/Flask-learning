from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime
from app import app, db
from app.forms import PostForm, EditProfileForm, EmptyForm
from app.models import User, Post

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author=current_user, body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('你的博客已提交')
        return redirect(url_for('index'))
    # 获得URL后的'?page=n'参数中的n
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='主页', posts=posts.items, form=form,
                           next_url=next_url, prev_url=prev_url
    )

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='浏览', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, int)
    posts = user.posts.paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('user', username=username, page=posts.next_num)\
        if posts.has_next else None
    prev_url = url_for('user', username=username, page=posts.prev_num)\
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items, form=form,
                           next_url=next_url, prev_url=prev_url)

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

@login_required
@app.route('/follow/<username>', methods=['POST'])
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit:
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'错误：未知用户{username}')
            return redirect(url_for('index'))
        if user == current_user:
            flash('错误：不能关注自己')
            return redirect(url_for('index'))
        if current_user.is_following(user):
            flash(f'您已经关注过 {username}')
        else:
            current_user.follow(user)
            db.session.commit()
            flash(f'已关注 {username}')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))

@login_required
@app.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    form = EmptyForm
    if form.validate_on_submit:
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'错误：找不到用户 {username}')
            return redirect(url_for('index'))
        if user == current_user:
            flash(f'错误：不能关注自己')
            return redirect(url_for('index'))
        if not current_user.is_following(user):
            flash('您尚未关注该用户')
        else:
            current_user.unfollow(user)
            db.session.commit()
            flash(f'成功取消对 {username} 的关注')
        return redirect(url_for('user', username=username))
