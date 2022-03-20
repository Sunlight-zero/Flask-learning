from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 用于输入用户的ID，返回用户对象
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140), default='这个人很懒，什么都没有写~')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        '''
        设置用户密码
        '''
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
