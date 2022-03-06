#!/usr/bin/env python3

# flake8: noqa

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('course', __name__, url_prefix='/course')
v = Validator(purge_unknown=True)

from . import create_course
