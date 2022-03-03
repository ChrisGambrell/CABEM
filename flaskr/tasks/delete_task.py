#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import db
from flaskr.tasks import bp
from flaskr.utils import owner


@bp.route('/<task_id>', methods=['DELETE'])
@owner
def delete_task(owned_task, **kwargs):
    db.session.delete(owned_task)
    db.session.commit()
    return jsonify({})
