from app import db, login, app
from time import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt


# 用于输入用户的ID，返回用户对象
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# 关注—被关注关系，使用辅助数据表
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# 用Python类储存数据库结构，这些类可以被ORM映射为数据库的对象
# 用户类将对应sql的一个关系（二维表），而用户的实例则对应表格的一行
class User(UserMixin, db.Model):
    '''
    存储网站的用户信息，并使用flask login处理用户登录功能
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db.relationship是一个特殊的关系，将两个数据表关联起来
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140), default='这个人很懒，什么都没有写~')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', # Right side class(entity) of the relationship, here is User itself
        # 用于建立关系的表格，这里为上面已经定义的followers辅助表
        secondary=followers,
        # 第一个类（实体）与followers表格的连接条件
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        '''
        设置用户密码
        '''
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except jwt.InvalidSignatureError:
            return
        return User.query.get(id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id))\
            .filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    '''
    存储网站的发帖信息
    '''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
