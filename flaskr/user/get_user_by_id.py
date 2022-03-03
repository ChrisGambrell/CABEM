#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import UserSchema
from flaskr.user import bp
from flaskr.utils import login_required, exists_user


@bp.route('/<user_id>', methods=['GET'])
@login_required
@exists_user
def get_user_by_id(fetched_user, **kwargs):
    return jsonify(UserSchema().dump(fetched_user))
