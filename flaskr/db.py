#!/usr/bin/env python3

import click
from datetime import datetime
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import update

metadata = MetaData(naming_convention={
    "ix": 'ix,%(column_0_label)s',
    "uq": "uq,%(table_name)s,%(column_0_name)s",
    "ck": "ck,%(table_name)s,%(constraint_name)s",
    "fk": "fk,%(table_name)s,%(column_0_name)s,%(referred_table_name)s",
    "pk": "pk,%(table_name)s",
})

db = SQLAlchemy(metadata=metadata)
mb = Marshmallow()


class Course(db.Model):
    idCourse = db.Column(db.Integer, nullable=False, primary_key=True)
    CourseTitle = db.Column(db.String(255), default=None)
    CourseStatus = db.Column(db.String(45), default=None)
    idProposal = db.Column(db.Integer, default=None)
    idProgram = db.Column(db.Integer, default=None)
    CourseNumber = db.Column(db.String(45), default=None)
    ProjectedStartDate = db.Column(db.DateTime, default=None)
    CourseStart = db.Column(db.DateTime, default=None)
    CourseEnd = db.Column(db.DateTime, default=None)
    isLaunched = db.Column(db.Integer, default='0')
    MarketingSignoff = db.Column(db.Integer, default='0')
    idUserMarketingSignoff = db.Column(db.Integer, default=None)
    DateMarketingSignoff = db.Column(db.DateTime, default=None)
    CMESignoff = db.Column(db.Integer, default='0')
    idUserCMESignoff = db.Column(db.Integer, default=None)
    DateCMESignoff = db.Column(db.DateTime, default=None)
    MedReviewSignoff = db.Column(db.Integer, default='0')
    idUserMedReviewSignoff = db.Column(db.Integer, default=None)
    DateMedReviewSignoff = db.Column(db.DateTime, default=None)
    AgendaComplete = db.Column(db.Integer, default='0')
    idUserAgendaComplete = db.Column(db.Integer, default=None)
    DateAgendaComplete = db.Column(db.DateTime, default=None)
    DateCreated = db.Column(db.DateTime, default=None)
    DateLastUpdated = db.Column(db.DateTime, default=None)
    idCourseType = db.Column(db.Integer, default=None)
    idUserCreated = db.Column(db.Integer, default=None)
    Renewal = db.Column(db.Integer, default='0')
    NASWApprovalNumber = db.Column(db.Integer, default=None)
    ProposalDueDate = db.Column(db.DateTime, default=None)
    idModule = db.Column(db.Integer, default=None)
    idWorkflowStep = db.Column(db.Integer, default=None)
    idPreviousWorkflowStep = db.Column(db.Integer, default=None)
    Valid = db.Column(db.Integer, default='1')
    idCVentEvent = db.Column(db.Integer, default=None)
    ClosureReason = db.Column(db.String(255), default=None)
    ClosureDescription = db.Column(db.String)
    CVentEventCode = db.Column(db.String(45), default=None)
    IsFree = db.Column(db.Integer, nullable=False, default='0')
    CatalogLinkout = db.Column(db.String(255), default=None)
    isLiveStream = db.Column(db.Integer, nullable=False, default='0')


class CourseSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_fk = True
        include_relationships = True


class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False, default='')
    Password = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Enabled = db.Column(db.Integer, nullable=False, default='1')
    LoggedIn = db.Column(db.Integer, nullable=False, default='0')
    SecurityQuestion = db.Column(db.String)
    SecurityAnswer = db.Column(db.String)
    StartDate = db.Column(db.DateTime, default=None)
    LastSeen = db.Column(db.DateTime, default=None)
    Img = db.Column(db.String(255), default=None)
    SaltKey = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(20), default=None)
    idAddress = db.Column(db.Integer, default=None)
    PasswordSetDate = db.Column(db.DateTime, default=datetime.utcnow())
    idSecurityQuestion = db.Column(db.Integer, nullable=False, default='0')
    RegistrationSent = db.Column(db.Integer, nullable=False, default='0')
    UseTwoFactor = db.Column(db.Integer, nullable=False, default='0')
    idUserDigestPreference = db.Column(db.Integer, default=None)
    isAdmin = db.Column(db.Integer, default='0')
    isLearner = db.Column(db.Integer, default='0')
    CourseMgt = db.Column(db.Integer, default='0')
    Registered = db.Column(db.Integer, nullable=False, default='0')
    DateOfBirth = db.Column(db.String(255), default=None)
    UpdatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


@event.listens_for(User, 'after_update')
def user_after_update(mapper, connection, user):
    @event.listens_for(Session, 'after_flush', once=True)
    def after_flush(session, context):
        session.execute(update(User).where(User.idUser == user.idUser).values(UpdatedAt=datetime.utcnow()))


class UserSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True


def init_data():
    # If any initial data is needed for the database,
    # do it here.
    # user = User(name='John Doe', username='jdoe', password='hashed_password')

    # db.session.add_all([user])
    pass


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
