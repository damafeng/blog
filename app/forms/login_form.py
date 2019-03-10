from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logger in')
    submit = SubmitField('Log In')


class EditProfileForm(FlaskForm):
    """编辑用户资料的form"""
    name = StringField('Name', validators=[DataRequired()])
    image = FileField('上传新头像')
    about = TextAreaField('About')
    submit = SubmitField('提交更改')
