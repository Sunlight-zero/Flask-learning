from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import app, db
from app.blogs import bp
from app.blogs.forms import PostForm
from app.models import Post

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author=current_user, body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('你的博客已提交')
        return redirect(url_for('blogs.index'))
    # 获得URL后的'?page=n'参数中的n
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('blogs.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blogs.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('blogs/index.html', title='主页', posts=posts.items, form=form,
                           next_url=next_url, prev_url=prev_url
    )

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('blogs.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blogs.explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('blogs/index.html', title='浏览', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
