#!/usr/bin/env python3

import pytest
from flaskr.db import Task, User
from tests.conftest import default_auth, default_user, parse_data


def test_get_user(user):
    response = user.get()
    data = parse_data(response)

    for key in ['name', 'username']:
        assert data[key] == default_auth[key]


@pytest.mark.parametrize(('data', 'status', 'error'), (
    ({'name': '', 'username': ''}, 400, {'name': ['empty values not allowed'], 'username': ['empty values not allowed']}),
    ({'name': 'Updating my name', 'username': 'username'}, 401, {'username': ['username is taken']}),
    ({'name': 'Updating my name', 'username': 'new_username'}, 200, {}),
))
def test_validate_edit_user_input(user, data, status, error):
    user.create()
    response = user.edit(data=data)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error


def test_edit_user(user):
    response = user.create()
    new_user = parse_data(response)

    response = user.edit(data={'name': 'New name', 'username': 'new username'})
    data = parse_data(response)

    for key in ['name', 'username']:
        assert data[key] != new_user[key]


def test_delete_user(user):
    user.create()
    num_users = User.query.count()
    user.delete()

    assert User.query.count() < num_users


def test_delete_user_cascade(task, user):
    response = user.create()
    new_user = parse_data(response)

    task.create(user=default_user)
    num_tasks = Task.query.filter_by(user_id=new_user['id']).count()
    user.delete()

    assert Task.query.filter_by(user_id=new_user['id']).count() < num_tasks


@pytest.mark.parametrize(('user_id', 'status', 'error'), (
    (-1, 404, {'user': ['user not found']}),
    (None, 200, {}),
))
def test_get_user_by_id(user, user_id, status, error):
    if user_id is not None:
        response = user.get_by_id(user_id=user_id)
        data = parse_data(response)

        assert response.status_code == status
        assert data.get('error', {}) == error
    else:
        response = user.create()
        new_user = parse_data(response)

        response = user.get_by_id(user_id=new_user['id'])
        fetched_user = parse_data(response)

        for key in fetched_user.keys():
            assert fetched_user[key] == new_user[key]
