#!/usr/bin/env python3

from flask import jsonify
from flaskr.api.course import bp
from flaskr.db import CourseSchema
from flaskr.utils import exists_course, login_required


@bp.route('/<course_id>', methods=['GET'])
@login_required
@exists_course
def get_course_by_id(fetched_course, **kwargs):
    return jsonify(CourseSchema().dump(fetched_course))
