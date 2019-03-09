from . import Model
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('email', str, ''),
    ]

    @classmethod
    def login(cls, email, password, permanent=False):
        print('email', email)
        print('password', password)
        print('permanent', permanent)
        u = cls.find_by(email=email)
        print('find u is ', u)
        if u is None:
            return False
        elif check_password_hash(u.password, password):
            session['user_id'] = u.id
            session.permanent = permanent
            return True
        else:
            return False

    @classmethod
    def logout(cls):
        session['user_id'] = -1
        session.permanent = False

    @classmethod
    def register(cls, form):
        form['password'] = generate_password_hash(form['password'])
        return cls.new(form)
