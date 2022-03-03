#!/usr/bin/env python3

import os
import pytest
import tempfile
from flaskr import create_app
from flaskr.db import Task, User, db


def parse_data(response):
    return response.get_json() if response.get_json() is not None else {}


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////{}'.format(db_path),
    })

    with app.app_context():
        db.create_all()

        user1 = User(name='user', username='username', password='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155')
        user2 = User(name='user2', username='username2', password='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155')
        task = Task(user=user1, body='test title')

        db.session.add_all([user1, user2, task])
        db.session.commit()

        yield app

        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


default_task = {
    'user': 1,
    'body': 'Test body',
}

default_auth = {
    'name': 'user',
    'username': 'username',
    'password': 'password',
}

default_user = {
    'name': 'John Doe',
    'username': 'jdoe',
    'password': 'password',
}


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def get_auth_header(self, user=default_auth):
        response = self.login(data=user)
        data = parse_data(response)

        return {'Authorization': f'Bearer {data.get("token", "")}'}

    def login(self, data=default_auth):
        return self._client.post('/auth/login', json=data)

    def register(self, data=default_user):
        return self._client.post('/auth/register', json=data)


@pytest.fixture()
def auth(client):
    return AuthActions(client)


class TaskActions(object):
    def __init__(self, client, auth):
        self._client = client
        self._auth = auth

    def get(self, user=default_auth):
        return self._client.get('/tasks/', headers=self._auth.get_auth_header(user=user))

    def get_by_id(self, task_id=1, user=default_auth):
        return self._client.get(f'/tasks/{task_id}', headers=self._auth.get_auth_header(user=user))

    def create(self, user=default_auth, data=default_task):
        return self._client.post('/tasks/', headers=self._auth.get_auth_header(user=user), json=data)

    def edit(self, task_id=1, user=default_auth, data=None):
        return self._client.patch(f'/tasks/{task_id}', headers=self._auth.get_auth_header(user=user), json=data)

    def delete(self, task_id=1, user=default_auth):
        return self._client.delete(f'/tasks/{task_id}', headers=self._auth.get_auth_header(user=user))


@pytest.fixture()
def task(client, auth):
    return TaskActions(client, auth)


class UserActions(object):
    def __init__(self, client, auth):
        self._client = client
        self._auth = auth

    def get(self, user=default_auth):
        return self._client.get('/user/', headers=self._auth.get_auth_header(user=user))

    def get_by_id(self, user_id=1, user=default_auth):
        return self._client.get(f'/user/{user_id}', headers=self._auth.get_auth_header(user=user))

    def create(self, data=default_user):
        return self._auth.register(data=data)

    def edit(self, user=default_user, data=None):
        return self._client.patch('/user/', headers=self._auth.get_auth_header(user=user), json=data)

    def delete(self, user=default_user):
        return self._client.delete('/user/', headers=self._auth.get_auth_header(user=user))


@pytest.fixture()
def user(client, auth):
    return UserActions(client, auth)
