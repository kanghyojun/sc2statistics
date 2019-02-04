# -*- coding: utf-8 -*-
from sc2web.replay import Replay
from sc2web.web.app import app

from .util import url_for


def test_upload_replay(f_replay, f_session):
    url = url_for('analyze_replays')
    with app.test_client() as c:
        r = c.post(
                url,
                content_type='multipart/form-data',
                data={'replay': f_replay})
    assert 302 == r.status_code
    loc = r.headers.get('Location', None)
    assert loc
    replay = f_session.query(Replay).first()
    assert replay
    assert replay.id in loc
