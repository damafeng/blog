from flask import flash, redirect, url_for, abort, session
from app.forms.login_form import LoginForm, EditProfileForm
from ..forms.register_form import RegisterForm
from ..models.user import User
from ..utils import render_template_with_statue, current_user, require_login
from . import main


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.login(form.email.data, form.password.data, form.remember_me.data):
            flash('Welcome, Login Succeed')
            return redirect(session.get('next') or url_for('main.index'))
        flash('Invalid email or password')
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
        flash('You Can now login. ')
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
    return render_template_with_statue('user.html', user=user, is_current_user=is_current_user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@require_login
def edit_profile():
    user = current_user()
    form = EditProfileForm()
    if form.validate_on_submit():
        update_form = {
            'name': form.name.data,
            'about': form.about.data,
        }
        user.update(update_form)
        flash('资料更新完成')
        return redirect(url_for('.user_profile', u_id=user.id))
    form.name.data = user.name
    form.about.data = user.about
    return render_template_with_statue('edit_profile.html', form=form)
