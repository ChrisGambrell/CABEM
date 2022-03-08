#!/usr/bin/env python3

import pytest
from datetime import datetime, timedelta
from flaskr.db import Course
from tests.conftest import default_auth, default_user, parse_data


@pytest.mark.parametrize(('CourseTitle', 'CourseNumber', 'CourseStart', 'CourseEnd', 'status', 'error'), (
    ('', '', 0, 0, 400, {'CourseTitle': ['empty values not allowed'], 'CourseNumber': ['empty values not allowed']}),
    ('Sample Title', 1234, datetime.now().timestamp() ,(datetime.now() + timedelta(days=30)).timestamp(), 200, {}),
))
def test_validate_create_course_input(course, CourseTitle, CourseNumber, CourseStart, CourseEnd, status, error):
    response = course.create(data={'CourseTitle': CourseTitle, 'CourseNumber': CourseNumber, 'CourseStart': CourseStart, 'CourseEnd': CourseEnd})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error


def test_create(course):
    num_courses = Course.query.count()
    course.create()

    assert Course.query.count() > num_courses


# # TODO - This is a failing test, needs to be debugged
# #        Imported from test_user
# def test_get_user(user):
#     response = user.get()
#     data = parse_data(response)

#     for key in ['Email', 'FirstName', 'LastName']:
#         assert data[key] == default_auth[key]


@pytest.mark.parametrize(('data', 'status', 'error'), (
    ({'CourseTitle': '', 'CourseNumber': ''}, 400, {'CourseTitle': ['empty values not allowed'], 'CourseNumber': ['empty values not allowed']}),
    ({'CourseTitle': 'New Course Title', 'CourseNumber': 987, 'CourseStart': (datetime.now() + timedelta(days=1)).timestamp()}, 200, {}),
))
def test_validate_edit_course_input(course, data, status, error):
    response = course.edit(data=data)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error


def test_edit_course(course):
    response = course.create()
    new_course = parse_data(response)

    response = course.edit(data={'CourseTitle': 'New Course Title', 'CourseNumber': 987, 'StartDate': (datetime.now() + timedelta(days=1)).timestamp()})
    data = parse_data(response)

    for key in ['CourseTitle', 'CourseNumber', 'CourseStart']:
        assert data[key] != new_course[key]


def test_delete_user(course):
    response = course.create()
    new_course = parse_data(response)

    num_courses = Course.query.count()
    course.delete(course_id=new_course['idCourse'])

    assert Course.query.count() < num_courses


@pytest.mark.parametrize(('course_id', 'status', 'error'), (
    (-1, 404, {'course': ['course not found']}),
    (None, 200, {}),
))
def test_get_course_by_id(course, course_id, status, error):
    if course_id is not None:
        response = course.get_by_id(course_id=course_id)
        data = parse_data(response)

        assert response.status_code == status
        assert data.get('error', {}) == error
    else:
        response = course.create()
        new_course = parse_data(response)

        response = course.get_by_id(course_id=new_course['idCourse'])
        fetched_course = parse_data(response)

        for key in fetched_course.keys():
            assert fetched_course[key] == new_course[key]
