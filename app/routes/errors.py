from . import main
from ..utils import render_template_with_statue


@main.app_errorhandler(404)
def page_not_found(e):
    error_str = 'NOT FOUND'
    return render_template_with_statue('error.html', error_str=error_str), 404
