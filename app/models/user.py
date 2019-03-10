from . import Model
from .role import Role, Permission
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('email', str, ''),
        ('role_id', int, 0),
        ('permission', int, 0),
    ]

    @classmethod
    def login(cls, email, password, permanent=False):
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
        role = Role.find_by(default=True)
        form['role_id'] = role.id
        form['permission'] = role.permission
        return cls.new(form)

    # 用户权限验证
    def can(self, permissions):
        return self.role_id != 0 and \
               (self.permission & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
