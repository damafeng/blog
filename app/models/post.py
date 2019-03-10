from . import Model
from .user import User
import datetime


class Post(Model):
    __fields__ = Model.__fields__ + [
        ('body', str, ''),
        ('author_id', int, -1),
    ]

    def get_author(self):
        return User.find_by(id=self.author_id)

    def ut_to_utc(self):
        utc = datetime.datetime.utcfromtimestamp(self.ut)
        return utc

    @staticmethod
    def page_post(page, sort='ut',
                  order='des', page_size=10, **kwargs):
        posts = Post.find_all(sort, order,
                              page_size, page_no=page, **kwargs)
        return posts
