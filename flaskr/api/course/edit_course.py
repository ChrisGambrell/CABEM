#!/usr/bin/env python3

from flask import jsonify
from flaskr.api.course import bp, request_schema, v
from flaskr.db import db, CourseSchema
from flaskr.utils import exists_course, login_required, parse_data


@bp.route('/<course_id>', methods=['PATCH'])
@login_required
@exists_course
@parse_data
def edit_course(fetched_course, data, **kwargs):
    if not v.validate(data, request_schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, request_schema)

    for key in data.keys():
        setattr(fetched_course, key, data[key])
    db.session.commit()

    return jsonify(CourseSchema().dump(fetched_course))
