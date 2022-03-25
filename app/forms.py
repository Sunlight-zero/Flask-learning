from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')

class RegisrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入您的用户名')])
    email = StringField('邮箱', validators=[
        DataRequired('请输入您的邮箱'), 
        Email('请使用正确格式的邮箱')
    ])
    password = PasswordField('密码', validators=[DataRequired('请输入您的密码')])
    repeat_password = PasswordField('确认密码', validators=[
        DataRequired('请再次确认密码'), 
        EqualTo('password', message='两次密码不一致，请重新检查您的密码')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册，请换一个用户名')
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('该邮箱已被注册，请换一个邮箱')

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('个人简介', validators=[Length(0, 140)])
    submit = SubmitField('提交')

    # 这样定义时，这个类初始化时应该传入一个参数，对应routes传入的current_user.username
    def __init__(self, origin_username: str, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.origin_username = origin_username

    def validate_username(self, username):
        if username.data != self.origin_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已被使用，请换一个用户名。')

class EmptyForm(FlaskForm):
    submit = SubmitField('提交')
