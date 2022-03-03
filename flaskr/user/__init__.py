#!/usr/bin/env python3

# flake8: noqa

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')
v = Validator(purge_unknown=True)

from . import delete_user
from . import edit_user
from . import get_user_by_id
from . import get_user
