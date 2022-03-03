#!/usr/bin/env python3

import click
from datetime import datetime
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete, update

db = SQLAlchemy()
mb = Marshmallow()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # noqa: A003
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    tasks = db.relationship('Task', back_populates='user')


@event.listens_for(User, 'after_update')
def user_after_update(mapper, connection, user):
    @event.listens_for(Session, 'after_flush', once=True)
    def after_flush(session, context):
        session.execute(update(User).where(User.id == user.id).values(updated_at=datetime.utcnow()))


@event.listens_for(User, 'after_delete')
def user_after_delete(mapper, connection, user):
    @event.listens_for(Session, 'after_flush', once=True)
    def after_flush(session, context):
        session.execute(delete(Task).where(Task.id.in_([task.id for task in user.tasks])))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # noqa: A003
    user = db.relationship('User', back_populates='tasks')
    body = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@event.listens_for(Task, 'after_update')
def task_after_update(mapper, connection, task):
    @event.listens_for(Session, 'after_flush', once=True)
    def task_after_flush(session, context):
        session.execute(update(Task).where(Task.id == task.id).values(updated_at=datetime.utcnow()))


class UserSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True


class TaskSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        include_relationships = True


def init_data():
    # If any initial data is needed for the database,
    # do it here.
    user = User(name='John Doe', username='jdoe', password='hashed_password')
    task = Task(user=user, body='Sample task', completed=True)

    db.session.add_all([user, task])


def init_db():
    # Uncomment if you want the database to reset
    # each time the app is started
    # db.drop_all()

    try:
        db.create_all()
        db.init_data()
    except Exception:
        pass


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    mb.init_app(app)
    init_db()
    app.cli.add_command(init_db_command)
