#!/usr/bin/env python3

# flake8: noqa

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('tasks', __name__, url_prefix='/tasks')
v = Validator(purge_unknown=True)

from . import create_task
from . import delete_task
from . import edit_task
from . import get_task_by_id
from . import get_tasks
