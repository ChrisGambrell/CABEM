#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import db, TaskSchema
from flaskr.tasks import bp, v
from flaskr.utils import owner, parse_data


@bp.route('/<task_id>', methods=['PATCH'])
@owner
@parse_data
def edit_task(owned_task, data, **kwargs):
    schema = {
        'body': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'completed': {
            'type': 'boolean',
            'coerce': bool,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    for key in data.keys():
        setattr(owned_task, key, data[key])
    db.session.commit()

    return jsonify(TaskSchema().dump(owned_task))
