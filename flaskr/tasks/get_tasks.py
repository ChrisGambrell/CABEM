#!/usr/bin/env python3

from flask import jsonify
from flaskr.db import Task, TaskSchema
from flaskr.tasks import bp
from flaskr.utils import login_required


@bp.route('/', methods=['GET'])
@login_required
def get_tasks(authed_user, **kwargs):
    tasks = Task.query.filter_by(user_id=authed_user.id)
    return jsonify(TaskSchema(many=True).dump(tasks))
