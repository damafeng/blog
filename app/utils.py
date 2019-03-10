from flask import session, render_template, abort
from .models.user import User
from functools import wraps


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


# 检查权限的装饰器
def permission_required(permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            log('permissions', permissions)
            log('user_permission', current_user().permission)
            if not current_user().can(permissions):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def render_template_with_statue(*args, **kwargs):
    is_login = current_user() is not None
    return render_template(*args, is_login=is_login, **kwargs)

