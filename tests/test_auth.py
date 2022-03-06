#!/usr/bin/env python3

import pytest
from flaskr.db import User
from tests.conftest import parse_data


@pytest.mark.parametrize(('Email', 'Password', 'status', 'error'), (
    ('', '', 400, {'Email': ['empty values not allowed'], 'Password': ['empty values not allowed']}),
    ('foobar@example.com', 'password', 401, {'Email': ['Email is incorrect']}),
    ('user@example.com', 'foobar', 401, {'Password': ['Password is incorrect.']}),
    ('user@example.com', 'password', 200, {}),
))
def test_validate_login_input(auth, Email, Password, status, error):
    response = auth.login(data={'Email': Email, 'Password': Password})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error
