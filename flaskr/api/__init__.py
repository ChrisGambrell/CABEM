#!/usr/bin/env python3

from flask import Blueprint
from . import auth, course, user

bp = Blueprint('api', __name__, url_prefix='/api')

bp.register_blueprint(auth.bp)
bp.register_blueprint(course.bp)
bp.register_blueprint(user.bp)
