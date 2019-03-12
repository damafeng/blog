from . import main
from flask import abort, request, redirect, url_for
from app.models.post import Post
from app.models.comment import Comment
from app.pagination import Pagination
from app.forms.comment_form import CommentForm
from ..utils import render_template_with_statue, current_user


@main.route('/post/<int:p_id>', methods=['GET', 'POST'])
def post(p_id):
    p = Post.find_by(id=p_id)
    if p is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        u = current_user()
        comment = {
            'body': form.body.data,
            'post_id': p_id,
            'user_id': u.id,
        }
        Comment.new(comment)
        return redirect(url_for('main.post', p_id=p_id))
    count = Comment.count(post_id=p_id)
    page = request.args.get('page', 1, type=int)
    comments = p.comments(page=page)
    pagination = Pagination.get_pagination(page, count)
    return render_template_with_statue('post_detail.html',
                                       post=p,
                                       form=form,
                                       comments=comments,
                                       pagination=pagination)
