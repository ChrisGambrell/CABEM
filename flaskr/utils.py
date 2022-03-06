#!/usr/bin/env python3

import functools
import jwt
import os
from dotenv import dotenv_values
from flask import jsonify, request
from flaskr.db import User


def exists_user(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        user = User.query.filter_by(idUser=kwargs.get('user_id', '')).first()
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
            decoded_user = User.query.filter_by(idUser=decoded_token.get('user_id', '')).first()

            if decoded_user is None:
                return jsonify({'error': {'user': ['user not found']}}), 404
            elif decoded_user.Password != decoded_token.get('Password', ''):
                return jsonify({'error': {'auth': ['unauthorized']}}), 401

            return endpoint(authed_user=decoded_user, **kwargs)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'error': {'auth': ['token expired']}}), 400
        except jwt.exceptions.DecodeError:
            return jsonify({'error': {'auth': ['invalid token']}}), 400
    return wrapped_endpoint


def parse_data(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        data = request.get_json() if request.get_json() is not None else {}
        return endpoint(data=data, **kwargs)
    return wrapped_endpoint
