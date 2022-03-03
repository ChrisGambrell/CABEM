#!/usr/bin/env python3

import os
from flask import Flask
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////{}'.format(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(app.instance_path))), 'instance', 'flaskr.sqlite'))).replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

with app.app_context():
    from flaskr import db

    db.init_app(app)
    migrate = Migrate(app, db.db)
