#!/usr/bin/env python3

from datetime import datetime
from flask import jsonify
from flaskr.user import bp, v
from flaskr.db import db, User, UserSchema
from flaskr.utils import parse_data
from werkzeug.security import generate_password_hash


@bp.route('/', methods=['POST'])
@parse_data
def create_user(data, **kwargs):
    schema = {
        'Email': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'Password': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'FirstName': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'LastName': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'SecurityQuestion': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'SecurityAnswer': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'StartDate': {
            'type': 'datetime',
            'coerce': datetime,
            'empty': False,
        },
        'Img': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'SaltKey': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'Phone': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'CourseMgt': {
            'type': 'integer',
            'coerce': int,
            'empty': False,
        },
        'DateOfBirth': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    if User.query.filter_by(Email=data['Email']).count() > 0:
        return jsonify({'error': {'Email': ['Email is taken']}}), 401

    data['Password'] = generate_password_hash(data['Password'])
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(UserSchema().dump(new_user))
