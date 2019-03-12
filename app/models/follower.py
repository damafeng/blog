from . import Model


class Follows(Model):
    __fields__ = Model.__fields__ + [
        ('follower_id', int, -1),
        ('followed_id', int, -1),
    ]

    @classmethod
    def change_follow(cls, follower_id, followed_id):
        form = {
            'follower_id': follower_id,
            'followed_id': followed_id,
        }
        r = Follows.find_by(all_data=True, **form)
        if r is None:
            return Follows.new(form)
        r.delete = not r.delete
        return r.save()
