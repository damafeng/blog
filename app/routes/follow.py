from . import main
from ..utils import current_user, require_login
from ..models.follower import Follows
from flask import jsonify, request, abort


@main.route('/change_follow', methods=['POST'])
def follow():
    u_id = int(request.data.decode('utf-8').split('"')[1])
    u = current_user()
    r = Follows.change_follow(u.id, u_id)
    if r is None:
        abort(404)
    return jsonify({'statue': 200})
