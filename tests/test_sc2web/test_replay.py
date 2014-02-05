# -*- coding: utf-8 -*-
from flask import json

from sc2web.web.app import app
from sc2web.replay import Replay

from .util import url_for


def test_upload_replay(f_replay, f_session):
    url = url_for('analyze_replays')
    with app.test_client() as c, f_replay as f:
        r = c.post(
                url,
                content_type='multipart/form-data',
                data={'replay': f})
    assert 302 == r.status_code
    loc = r.headers.get('Location', None)
    assert loc
    replay = f_session.query(Replay).first()
    assert replay
    assert replay.id in loc
