#!/usr/bin/env python3

# flake8: noqa

from cerberus import Validator
from datetime import datetime
from flask import Blueprint

bp = Blueprint('course', __name__, url_prefix='/course')
v = Validator(purge_unknown=True)

request_schema = {
    'CourseTitle': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'CourseStatus': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'idProposal': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idProgram': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'CourseNumber': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'ProjectedStartDate': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'CourseStart': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'CourseEnd': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'isLaunched': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'MarketingSignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idUserMarketingSignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'DateMarketingSignoff': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'CMESignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idUserCMESignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'DateCMESignoff': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'MedReviewSignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idUserMedReviewSignoff': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'DateMedReviewSignoff': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'AgendaComplete': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idUserAgendaComplete': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'DateAgendaComplete': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'DateCreated': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'DateLastUpdated': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'idCourseType': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idUserCreated': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'Renewal': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'NASWApprovalNumber': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'ProposalDueDate': {
        'type': 'datetime',
        'coerce': datetime,
        'empty': False,
    },
    'idModule': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idWorkflowStep': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idPreviousWorkflowStep': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'Valid': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'idCVentEvent': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'ClosureReason': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'ClosureDescription': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'CVentEventCode': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'IsFree': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    },
    'CatalogLinkout': {
        'type': 'string',
        'coerce': str,
        'empty': False,
    },
    'isLiveStream': {
        'type': 'integer',
        'coerce': int,
        'empty': False,
    }
}

from . import create_course
from . import delete_course
from . import edit_course
from . import get_courses
from . import get_course_by_id
