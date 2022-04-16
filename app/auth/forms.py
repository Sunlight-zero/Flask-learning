from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('重置密码')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired()])
    repeat_password = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置密码')
