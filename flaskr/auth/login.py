#!/usr/bin/env python3

import jwt
import os
from datetime import datetime, timedelta
from dotenv.main import dotenv_values
from flask import jsonify
from flaskr.auth import bp, v
from flaskr.db import User
from flaskr.utils import parse_data
from werkzeug.security import check_password_hash


@bp.route('/login', methods=['POST'])
@parse_data
def login(data, **kwargs):
    schema = {
        'Email': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'Password': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    user = User.query.filter_by(Email=data['Email']).first()

    if user is None:
        return jsonify({'error': {'Email': ['Email is incorrect']}}), 401
    elif not check_password_hash(user.Password, data['Password']):
        return jsonify({'error': {'Password': ['Password is incorrect.']}}), 401

    return jsonify({'token': jwt.encode({
        'user_id': user.idUser,
        'Password': user.Password,
        'exp': (datetime.now() + timedelta(days=30)).timestamp(),
    }, os.getenv('AUTH_SECRET', dotenv_values().get('AUTH_SECRET')), algorithm='HS256')})
