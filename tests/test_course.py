#!/usr/bin/env python3

import pytest
from datetime import datetime, timedelta
from flaskr.db import  User
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


# def test_create(user):
#     num_users = User.query.count()
#     user.create()

#     assert User.query.count() > num_users


# # # TODO - This is a failing test, needs to be debugged
# # def test_get_user(user):
# #     response = user.get()
# #     data = parse_data(response)

# #     for key in ['Email', 'FirstName', 'LastName']:
# #         assert data[key] == default_auth[key]


# @pytest.mark.parametrize(('data', 'status', 'error'), (
#     ({'Email': '', 'FirstName': '', 'LastName': ''}, 400, {'Email': ['empty values not allowed'], 'FirstName': ['empty values not allowed'], 'LastName': ['empty values not allowed']}),
#     ({'Email': 'user@example.com', 'FirstName': 'Johnny', 'LastName': 'Dowe'}, 401, {'Email': ['Email is taken']}),
#     ({'Email': 'new_user@example.com', 'FirstName': 'Johnny', 'LastName': 'Dowe'}, 200, {}),
# ))
# def test_validate_edit_user_input(user, data, status, error):
#     user.create()
#     response = user.edit(data=data)
#     data = parse_data(response)

#     assert response.status_code == status
#     assert data.get('error', {}) == error


# def test_edit_user(user):
#     response = user.create()
#     new_user = parse_data(response)

#     response = user.edit(data={'Email': 'new_user@example.com', 'FirstName': 'Johnny', 'LastName': 'Dowe'})
#     data = parse_data(response)

#     for key in ['Email', 'FirstName', 'LastName']:
#         assert data[key] != new_user[key]


# def test_delete_user(user):
#     user.create()
#     num_users = User.query.count()
#     user.delete()

#     assert User.query.count() < num_users


# @pytest.mark.parametrize(('user_id', 'status', 'error'), (
#     (-1, 404, {'user': ['user not found']}),
#     (None, 200, {}),
# ))
# def test_get_user_by_id(user, user_id, status, error):
#     if user_id is not None:
#         response = user.get_by_id(user_id=user_id)
#         data = parse_data(response)

#         assert response.status_code == status
#         assert data.get('error', {}) == error
#     else:
#         response = user.create()
#         new_user = parse_data(response)

#         response = user.get_by_id(user_id=new_user['idUser'])
#         fetched_user = parse_data(response)

#         for key in fetched_user.keys():
#             assert fetched_user[key] == new_user[key]
