from flask import flash, redirect, url_for, abort, session, request
from app.forms.user_form import LoginForm, RegisterForm
from ..forms.edit_profile_form import EditProfileForm
from ..models.user import User
from ..models.post import Post
from ..pagination import Pagination
from ..utils import render_template_with_statue, current_user, require_login
from . import main


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.login(form.email.data, form.password.data, form.remember_me.data):
            flash('欢迎来到我的酒馆')
            return redirect(session.get('next') or url_for('main.index'))
        flash('邮箱或者密码错误')
    return render_template_with_statue('login.html', form=form)


@main.route('/logout')
def logout():
    u = current_user()
    u.logout()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        register_form = {
            'email': form.email.data,
            'username': form.username.data,
            'password': form.password.data,
        }
        User.register(register_form)
        flash('注册成功，可以登录了')
        return redirect(url_for('.login'))
    return render_template_with_statue('register.html', form=form)


@main.route('/user/<int:u_id>')
def user_profile(u_id):
    user = User.find_by(id=u_id)
    if user is None:
        abort(404)
    cu = current_user()
    if cu is not None and cu.owner(u_id):
        is_current_user = True
    else:
        is_current_user = False
    count = user.data_count(Post)
    page = request.args.get('page', 1, type=int)
    posts = Post.page_post(page=page, user_id=u_id)
    pagination = Pagination.get_pagination(page, count)
    return render_template_with_statue('user.html',
                                       user=user,
                                       is_current_user=is_current_user,
                                       posts=posts,
                                       pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@require_login
def edit_profile():
    user = current_user()
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.about = form.about.data
        user.save()
        flash('资料更新完成')
        return redirect(url_for('.user_profile', u_id=user.id))
    form.name.data = user.name
    form.about.data = user.about
    return render_template_with_statue('edit_profile.html', form=form)

