from .post import Post


class Comment(Post):
    __fields__ = Post.__fields__ + [
        ('post_id', int, -1),
    ]
