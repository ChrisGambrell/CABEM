#!/usr/bin/env python3

from flaskr import create_app
from flaskr.db import init_db


def test_init_db():
    app = create_app()
    with app.app_context():
        assert init_db() is None


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialized the database.\n' == result.output
    assert Recorder.called
