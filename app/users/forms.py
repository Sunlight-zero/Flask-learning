from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

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
