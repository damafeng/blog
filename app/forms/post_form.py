from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('文章标题', validators=[DataRequired()])
    body = TextAreaField("文章内容", validators=[DataRequired()])
    submit = SubmitField('提交')
