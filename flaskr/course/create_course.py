#!/usr/bin/env python3

from flask import jsonify
from flaskr.course import bp, request_schema, v
from flaskr.db import db, Course, CourseSchema
from flaskr.utils import login_required, parse_data


@bp.route('/', methods=['POST'])
@login_required
@parse_data
def create_course(data, **kwargs):
    if not v.validate(data, request_schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, request_schema)

    new_course = Course(**data)
    db.session.add(new_course)
    db.session.commit()

    return jsonify(CourseSchema().dump(new_course))
