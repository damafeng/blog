from flask_wtf import FlaskForm
from ..models.user import User
from wtforms import (
    PasswordField,
    StringField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    Email,
    DataRequired,
    Length,
    Regexp,
    EqualTo,
    ValidationError, )


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    # email 验证非空， 格式， 长度
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email(),
        Length(1, 64),
    ])
    # username 验证非空，长度, 格式
    username = StringField('帐号', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '字母开头，且只能包含字母数字下划线'),
    ])
    # 验证非空， 和Confirm Password相同
    password = PasswordField('密码', validators=[
        DataRequired(),
        EqualTo('password2', message='两次密码不同')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
    ])
    submit = SubmitField('登录')

    # validate_ 开头且跟字段名的方法, 在validate_on_submit时会自动调用
    def validate_username(self, field):
        if User.find_by(username=field.data) is not None:
            raise ValidationError('帐号已经注册过了')

    def validate_email(self, field):
        if User.find_by(email=field.data) is not None:
            raise ValidationError('邮箱已经注册过了')
