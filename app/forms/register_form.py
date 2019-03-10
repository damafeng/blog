from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     StringField,
                     SubmitField,
                     ValidationError,
                     TextAreaField,
                     SelectField,)
from wtforms.validators import Email, DataRequired, EqualTo, Length, Regexp
from ..models.user import User
from ..models.role import Role


class RegisterForm(FlaskForm):
    # email 验证非空， 格式， 长度
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 64),
    ])
    # username 验证非空，长度, 格式
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '字母开头，且只能包含字母数字下划线'),
    ])
    # 验证非空， 和Confirm Password相同
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password2', message='两次密码不同')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(),
    ])
    submit = SubmitField('Sign Up')

    # validate_ 开头且跟字段名的方法, 在validate_on_submit时会自动调用
    def validate_username(self, field):
        if User.find_by(username=field.data) is not None:
            raise ValidationError('Username already registered')

    def validate_email(self, field):
        if User.find_by(email=field.data) is not None:
            raise ValidationError('Email already registered')


class EditProfileAdminForm(FlaskForm):
    # email 验证非空， 格式， 长度
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 64),
    ])
    role = SelectField('Role', coerce=int)
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About')
    submit = SubmitField('更改信息')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name)
            for role in Role.all()
        ]
        self.user = user

    def validate_email(self, field):
        if self.email.data != self.user.email and \
                User.find_by(email=field.data) is not None:
            raise ValidationError('Email already registered')
