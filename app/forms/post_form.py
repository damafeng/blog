from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    body = TextAreaField("说点什么呗~", validators=[DataRequired()])
    submit = SubmitField('提交')
