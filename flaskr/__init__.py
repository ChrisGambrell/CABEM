#!/usr/bin/env python3

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flaskr.utils import parse_data


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////{}'.format(os.path.join(app.instance_path, 'flaskr.sqlite'))).replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    CORS(app)

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import db
        db.init_app(app)
        db.init_data()

        from flaskr.utils import login_required

        @app.route('/hello')
        def hello():
            return 'hello, world!'

        @app.route('/secret')
        @login_required
        @parse_data
        def secret(authed_user, **kwargs):
            return jsonify({'hello': authed_user.name})

        from . import auth
        app.register_blueprint(auth.bp)

        from . import tasks
        app.register_blueprint(tasks.bp)

        from . import user
        app.register_blueprint(user.bp)

    return app
