from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    post = TextAreaField('分享你的心情：', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('发表博客')