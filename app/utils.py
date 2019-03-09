from flask import session, render_template
from .models.user import User


def log(*args, **kwargs):
    print(*args, **kwargs)


def require_login():
    """
    当未登陆的时候跳转到登陆页面，且记录下当前位置
    :return:
    """
    pass


def current_user():
    """
    根据session找到本次请求的用户
    :return: user
    """
    u_id = int(session.get('user_id', -1))
    return User.find_by(id=u_id)


def render_template_with_statue(*args, **kwargs):
    is_login = current_user() is not None
    return render_template(*args, is_login=is_login, **kwargs)

