from flask import Blueprint
from ..models.role import Permission
from ..utils import current_user, render_template_with_statue, permission_required


main = Blueprint('main', __name__)

from . import user, errors


# 通过上下文将Permission设为模板中全局可访问
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


@main.route('/')
def index():
    u = current_user()
    return render_template_with_statue('index.html', user=u)
