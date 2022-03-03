#!/usr/bin/env python3

# flake8: noqa

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')
v = Validator(purge_unknown=True, require_all=True)

from . import login
from . import register
