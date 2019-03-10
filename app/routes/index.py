from . import main
from ..forms.post_form import PostForm
from ..utils import current_user, render_template_with_statue
from ..models.role import Permission
from ..models.post import Post
from flask import redirect, url_for, request


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    u = current_user()
    if u is not None \
            and u.can(Permission.WRITE) \
            and form.validate_on_submit():
        post = {
            'body': form.body.data,
            'author_id': u.id,
        }
        Post.new(post)
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.page_post(page)
    return render_template_with_statue('index.html', form=form, posts=posts)
