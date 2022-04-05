#!/usr/bin/env python3

from flask import jsonify
from flaskr.api.course import bp
from flaskr.db import Course, CourseSchema
from flaskr.utils import login_required


@bp.route('/', methods=['GET'])
# @login_required
def get_courses(**kwargs):
    return jsonify(CourseSchema(many=True).dump(Course.query.all()))
