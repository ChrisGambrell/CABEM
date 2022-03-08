#!/usr/bin/env python3

import os
import pytest
import tempfile
from datetime import datetime, timedelta
from flaskr import create_app
from flaskr.db import Course, User, db


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

        course1 = Course(CourseTitle='Course 1', CourseNumber='123')
        course2 = Course(CourseTitle='Course 2', CourseNumber='124')

        user1 = User(Email='user@example.com', Password='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', FirstName='User', LastName='Name', SecurityQuestion='', SecurityAnswer='', StartDate=None, Img='', SaltKey='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', Phone='', CourseMgt='', DateOfBirth='')
        user2 = User(Email='user2@example.com', Password='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', FirstName='User2', LastName='Name2', SecurityQuestion='', SecurityAnswer='', StartDate=None, Img='', SaltKey='pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', Phone='', CourseMgt='', DateOfBirth='')

        db.session.add_all([course1, course2, user1, user2])
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


default_auth = {
    'FirstName': 'User',
    'LastName': 'Name',
    'Email': 'user@example.com',
    'Password': 'password',
}

default_course = {
    'CourseTitle': 'Sample Course',
    'CourseNumber': 1234567890,
    'CourseStart': datetime.now(),
    'CourseEnd': datetime.now() + timedelta(days=30)
}

default_user = {
    'Email': 'jdoe@example.com',
    'Password': 'password',
    'FirstName': 'John',
    'LastName': 'Doe',
    'SaltKey': 'password',
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


@pytest.fixture()
def auth(client):
    return AuthActions(client)


class CourseActions(object):
    def __init__(self, client, auth):
        self._client = client
        self._auth = auth

    def create(self, user=default_auth, data=default_course):
        return self._client.post('/course/', json=data, headers=self._auth.get_auth_header(user=user))

    def get(self, user=default_auth):
        return self._client.get('/course/', headers=self._auth.get_auth_header(user=user))

    def get_by_id(self, course_id=1, user=default_auth):
        return self._client.get(f'/course/{course_id}', headers=self._auth.get_auth_header(user=user))

    def edit(self, course_id=1, user=default_auth, data=None):
        return self._client.patch(f'/course/{course_id}', json=data, headers=self._auth.get_auth_header(user=user))

    def delete(self, course_id, user=default_auth):
        return self._client.delete(f'/course/{course_id}', headers=self._auth.get_auth_header(user=user))


@pytest.fixture()
def course(client, auth):
    return CourseActions(client, auth)


class UserActions(object):
    def __init__(self, client, auth):
        self._client = client
        self._auth = auth

    def create(self, data=default_user):
        return self._client.post('/user/', json=data)

    def get(self, user=default_auth):
        return self._client.get('/user/', headers=self._auth.get_auth_header(user=user))

    def get_by_id(self, user_id=1, user=default_auth):
        return self._client.get(f'/user/{user_id}', headers=self._auth.get_auth_header(user=user))

    def edit(self, user=default_user, data=None):
        return self._client.patch('/user/', headers=self._auth.get_auth_header(user=user), json=data)

    def delete(self, user=default_user):
        return self._client.delete('/user/', headers=self._auth.get_auth_header(user=user))


@pytest.fixture()
def user(client, auth):
    return UserActions(client, auth)
