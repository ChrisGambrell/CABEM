#!/usr/bin/env python3

from datetime import datetime
from flask import jsonify
from flaskr.db import db, User, UserSchema
from flaskr.api.user import bp, v
from flaskr.utils import login_required, parse_data

to_datetime = lambda t: datetime.fromtimestamp(t)


@bp.route('/', methods=['PATCH'])
@login_required
@parse_data
def edit_user(authed_user, data, **kwargs):
    schema = {
        'Email': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'FirstName': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'LastName': {
            'type': 'string',
            'coerce': str,
            'empty': False,
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
            'coerce': to_datetime,
            'empty': False,
        },
        'Img': {
            'type': 'string',
            'coerce': str,
            'empty': False,
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

    for key in data.keys():
        if key == 'Email' and data['Email'] != authed_user.Email:
            if User.query.filter_by(Email=data[key]).count() > 0:
                return jsonify({'error': {'Email': ['Email is taken']}}), 401
        setattr(authed_user, key, data[key])
    db.session.commit()

    return jsonify(UserSchema().dump(authed_user))
