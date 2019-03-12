from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    ValidationError,
    TextAreaField,
    SelectField,
)
from wtforms.validators import Email, DataRequired, Length
from ..models.role import Role
from ..models.user import User


class EditProfileForm(FlaskForm):
    """编辑用户资料的form"""
    name = StringField('用户名', validators=[DataRequired()])
    about = TextAreaField('简介')
    submit = SubmitField('提交更改')


class EditProfileAdminForm(FlaskForm):
    # email 验证非空， 格式， 长度
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email(),
        Length(1, 64),
    ])
    role = SelectField('权限', coerce=int)
    name = StringField('用户名', validators=[DataRequired()])
    about = TextAreaField('简介')
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
            raise ValidationError('邮箱已经注册过了')
