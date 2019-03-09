from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logger in')
    submit = SubmitField('Log In')
