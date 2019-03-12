from . import main
from flask import abort
from app.models.post import Post
from ..utils import render_template_with_statue


@main.route('/post/<int:p_id>')
def post(p_id):
    p = Post.find_by(id=p_id)
    if p is None:
        abort(404)
    return render_template_with_statue('post_detail.html', post=p)
