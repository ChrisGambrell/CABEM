#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import db, User, UserSchema
from flaskr.user import bp, v
from flaskr.utils import login_required, parse_data


@bp.route('/', methods=['PATCH'])
@login_required
@parse_data
def edit_user(authed_user, data, **kwargs):
    schema = {
        'name': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'username': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    for key in data.keys():
        if key == 'username' and data['username'] != authed_user.username:
            if User.query.filter_by(username=data[key]).count() > 0:
                return jsonify({'error': {'username': ['username is taken']}}), 401
        setattr(authed_user, key, data[key])
    db.session.commit()

    return jsonify(UserSchema().dump(authed_user))
