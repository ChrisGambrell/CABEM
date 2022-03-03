#!/usr/bin/env python3

import pytest
from flaskr.db import User
from tests.conftest import parse_data


@pytest.mark.parametrize(('username', 'password', 'status', 'error'), (
    ('', '', 400, {'username': ['empty values not allowed'], 'password': ['empty values not allowed']}),
    ('foobar', 'password', 401, {'username': ['username is incorrect']}),
    ('username', 'foobar', 401, {'password': ['password is incorrect.']}),
    ('username', 'password', 200, {}),
))
def test_validate_login_input(auth, username, password, status, error):
    response = auth.login(data={'username': username, 'password': password})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error
