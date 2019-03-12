from flask import Blueprint
from ..models.role import Permission
from ..utils import current_user


main = Blueprint('main', __name__)

from . import user, errors, index, post, follow


# 通过上下文将Permission设为模板中全局可访问
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


# 通过上下文将is_admin设为模板中全局可访问
@main.app_context_processor
def inject_admin():
    def is_admin():
        return current_user() is not None \
               and current_user().is_administrator()
    return dict(is_admin=is_admin)


@main.before_app_request
def before_request():
    u = current_user()
    if u is not None:
        u.ping()
