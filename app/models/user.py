from . import Model
import time
from .role import Role, Permission
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('email', str, ''),
        ('name', str, ''),
        ('about', str, ''),
        ('member_since', int, 0),
        ('last_seen', int, 0),
        ('role_id', int, 0),
        ('permission', int, 0),
    ]

    @classmethod
    def login(cls, email, password, permanent=False):
        u = cls.find_by(email=email)
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
        u = cls.new(form)
        return u._init_user()

    # 用户权限验证
    def can(self, permissions):
        return self.role_id != 0 and \
               (self.permission & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def _init_user(self):
        form = {
            'name': '工号' + str(self.id),
            'about': '简单介绍下自己吧',
            'member_since': self.ct,
            'last_seen': self.ct,
        }
        return self.update(form)

    def ping(self):
        form = {
            'last_seen': int(time.time())
        }
        self.update(form)

    def time_info(self):
        from ..utils import str_time
        t = [
            'Member since : {}.'.format(str_time(self.member_since)),
            'Last seen : {}.'.format(str_time(self.last_seen, format_type=1))
        ]
        return t

    def owner(self, u_id):
        return self.id == u_id
