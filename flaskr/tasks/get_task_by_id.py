#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import TaskSchema
from flaskr.tasks import bp
from flaskr.utils import login_required, exists_task


@bp.route('/<task_id>', methods=['GET'])
@login_required
@exists_task
def get_task_by_id(fetched_task, **kwargs):
    return jsonify(TaskSchema().dump(fetched_task))
