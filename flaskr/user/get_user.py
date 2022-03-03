#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import UserSchema
from flaskr.user import bp
from flaskr.utils import login_required


@bp.route('/', methods=['GET'])
@login_required
def get_user(authed_user, **kwargs):
    return jsonify(UserSchema().dump(authed_user))
