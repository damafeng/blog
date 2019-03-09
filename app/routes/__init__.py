from flask import Blueprint
from ..utils import current_user, render_template_with_statue


main = Blueprint('main', __name__)

from . import user, errors


@main.route('/')
def index():
    u = current_user()
    return render_template_with_statue('index.html', user=u)
