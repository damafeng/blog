from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment


def generate_fake_user(count=50):
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
        d = {
            'email': forgery_py.internet.email_address(),
            'username': forgery_py.internet.user_name(),
            'password': forgery_py.lorem_ipsum.word(),
        }
        User.register(d)


def generate_fake_post(count=200):
    from random import seed, randint
    import forgery_py

    seed()
    for i in range(count):
        u = User.find_by(id=randint(1, 49))
        d = {
            'user_id': u.id,
            'body': forgery_py.lorem_ipsum.sentence(),
        }
        Post.new(d)


def generate_fake_comment(count=300):
    from random import seed, randint
    import forgery_py

    seed()
    for i in range(count):
        u = User.find_by(id=randint(1, 49))
        p = Post.find_by(id=randint(1, 199))
        d = {
            'user_id': u.id,
            'body': forgery_py.lorem_ipsum.sentence(),
            'post_id': p.id,
        }
        Comment.new(d)


if __name__ == '__main__':
    # generate_fake_user(50)
    # generate_fake_post(150)
    generate_fake_comment()

