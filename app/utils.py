from flask import session, render_template, abort, redirect, url_for, request
from .models.user import User
from functools import wraps
import time


def str_time(timestamp, format_type=2):
    time_format1 = '%Y/%m/%d %H h %M m'
    time_format2 = '%Y/%m/%d'
    value = time.localtime(timestamp)
    if format_type == 1:
        dt = time.strftime(time_format1, value)
    else:
        dt = time.strftime(time_format2, value)
    return dt


def log(*args, **kwargs):
    print(*args, **kwargs)


def current_user():
    """
    根据session找到本次请求的用户
    :return: user
    """
    u_id = int(session.get('user_id', -1))
    return User.find_by(id=u_id)


def require_login(f):
    """
    当未登陆的时候跳转到登陆页面，且记录下当前位置
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user() is None:
            session['next'] = request.path
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


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
    return render_template(*args, current_user=current_user(), **kwargs)

