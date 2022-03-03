#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import db, Task, TaskSchema
from flaskr.tasks import bp, v
from flaskr.utils import login_required, parse_data


@bp.route('/', methods=['POST'])
@login_required
@parse_data
def create_task(authed_user, data, **kwargs):
    schema = {
        'body': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'completed': {
            'type': 'boolean',
            'coerce': bool,
            'empty': False,
            'default': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    new_task = Task(user=authed_user, body=data['body'], completed=data['completed'])
    db.session.add(new_task)
    db.session.commit()

    return jsonify(TaskSchema().dump(new_task))
