#!/usr/bin/env python3

from flask import jsonify
from flaskr.auth import bp, v
from flaskr.db import db, User, UserSchema
from flaskr.utils import parse_data
from werkzeug.security import generate_password_hash


@bp.route('/register', methods=['POST'])
@parse_data
def register(data, **kwargs):
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
        'password': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    if User.query.filter_by(username=data['username']).count() > 0:
        return jsonify({'error': {'username': ['username is taken']}}), 401

    new_user = User(name=data['name'], username=data['username'], password=generate_password_hash(data['password']))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(UserSchema().dump(new_user))
