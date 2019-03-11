from . import Model
from flask import abort
from .user import User
import datetime


class Post(Model):
    __fields__ = Model.__fields__ + [
        ('body', str, ''),
        ('user_id', int, -1),
    ]

    def get_author(self):
        return User.find_by(id=self.user_id)

    def ut_to_utc(self):
        utc = datetime.datetime.utcfromtimestamp(self.ut)
        return utc

    @staticmethod
    def page_post(page, sort='ut',
                  order='des', page_size=10, **kwargs):
        posts = Post.find_all(sort, order,
                              page_size, page_no=page, **kwargs)
        if len(posts) == 0 and page != 1:
            abort(404)
        return posts

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            u = User.find_by(id=randint(1, 99))
            d = {
                'user_id': u.id,
                'body': forgery_py.lorem_ipsum.sentence(),
            }
            Post.new(d)
