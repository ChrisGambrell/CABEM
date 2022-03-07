#!/usr/bin/env python3

from datetime import datetime
from flask import jsonify
from flaskr.course import bp, v
from flaskr.db import db, Course, CourseSchema
from flaskr.utils import login_required, parse_data


@bp.route('/', methods=['POST'])
@login_required
@parse_data
def create_course(data, **kwargs):
    schema = {
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

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    new_course = Course(**data)
    db.session.add(new_course)
    db.session.commit()

    return jsonify(CourseSchema().dump(new_course))
