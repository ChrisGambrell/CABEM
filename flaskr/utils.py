#!/usr/bin/env python3

import functools
import jwt
import os
from dotenv import dotenv_values
from flask import jsonify, request
from flaskr.db import Task, User


def exists_task(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        task = Task.query.filter_by(id=kwargs.get('task_id', '')).first()
        if task is None:
            return jsonify({'error': {'task': ['task not found']}}), 404
        return endpoint(fetched_task=task, **kwargs)
    return wrapped_endpoint


def exists_user(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        user = User.query.filter_by(id=kwargs.get('user_id', '')).first()
        if user is None:
            return jsonify({'error': {'user': ['user not found']}}), 404
        return endpoint(fetched_user=user, **kwargs)
    return wrapped_endpoint


def login_required(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        authorization = request.headers.get('Authorization', '')
        if len(authorization.split('Bearer ')) > 1:
            token = authorization.split('Bearer ')[1]
        else:
            return jsonify({'error': {'auth': ['missing token']}}), 400

        try:
            decoded_token = jwt.decode(token, os.getenv('AUTH_SECRET', dotenv_values().get('AUTH_SECRET')), algorithms=['HS256'])
            decoded_user = User.query.filter_by(id=decoded_token.get('user_id', '')).first()

            if decoded_user is None:
                return jsonify({'error': {'user': ['user not found']}}), 404
            elif decoded_user.password != decoded_token.get('password', ''):
                return jsonify({'error': {'auth': ['unauthorized']}}), 401

            return endpoint(authed_user=decoded_user, **kwargs)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'error': {'auth': ['token expired']}}), 400
        except jwt.exceptions.DecodeError:
            return jsonify({'error': {'auth': ['invalid token']}}), 400
    return wrapped_endpoint


def owner(endpoint):
    @functools.wraps(endpoint)
    @login_required
    @exists_task
    def wrapped_endpoint(authed_user, fetched_task, **kwargs):
        if fetched_task.user_id != authed_user.id:
            return jsonify({'error': {'auth': ['access denied']}}), 401

        return endpoint(owned_task=fetched_task, **kwargs)
    return wrapped_endpoint


def parse_data(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        data = request.get_json() if request.get_json() is not None else {}
        return endpoint(data=data, **kwargs)
    return wrapped_endpoint
