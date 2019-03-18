from . import main
from ..utils import current_user, render_template_with_statue, require_login
from ..models.post import Post
from ..pagination import Pagination
from flask import redirect, url_for, request, make_response


@main.route('/', methods=['GET', 'POST'])
def index():
    u = current_user()
    show_followed = False
    if u is not None:
        show_followed = bool(request.cookies.get('show_followed', ''))
    page = request.args.get('page', 1, type=int)
    if show_followed:
        count, posts = u.followed_posts(page)
    else:
        count = Post.count()
        posts = Post.page_post(page)

    pagination = Pagination.get_pagination(page, count)
    return render_template_with_statue('index.html',
                                       posts=posts,
                                       pagination=pagination,
                                       show_followed=show_followed)


@main.route('/all')
def show_all():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '', max_age=24*60*60)
    return resp


@main.route('/followed')
@require_login
def show_followed():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '1', max_age=24*60*60)
    return resp
