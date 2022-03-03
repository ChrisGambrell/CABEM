#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import db
from flaskr.user import bp
from flaskr.utils import login_required


@bp.route('/', methods=['DELETE'])
@login_required
def delete_user(authed_user, **kwargs):
    db.session.delete(authed_user)
    db.session.commit()
    return jsonify({})
