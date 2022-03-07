#!/usr/bin/env python3

from flask import jsonify
from flaskr.course import bp
from flaskr.db import db
from flaskr.utils import exists_course, login_required


@bp.route('/<course_id>', methods=['DELETE'])
@login_required
@exists_course
def delete_course(fetched_course, **kwargs):
    db.session.delete(fetched_course)
    db.session.commit()
    return jsonify({})
