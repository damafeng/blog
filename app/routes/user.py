from flask import flash, redirect, url_for
from app.forms.login_form import LoginForm
from ..forms.register_form import RegisterForm
from ..models.user import User
from ..utils import render_template_with_statue, current_user
from . import main


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.login(form.email.data, form.password.data, form.remember_me.data):
            flash('Welcome, Login Succeed')
            return redirect(url_for('main.index'))
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
