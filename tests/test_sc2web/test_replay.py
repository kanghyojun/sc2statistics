# -*- coding: utf-8 -*-
from flask import json

from sc2web.web.app import app

from .util import url_for


def test_upload_replay(f_replay):
    url = url_for('analyze_replay')
    with app.test_client() as c, f_replay as f:
        r = c.post(
                url,
                content_type='multipart/form-data',
                data={'replay': f})
    assert 200 == r.status_code
    json_ = json.loads(r.data)
    assert 'build' in json_
    print json_
    assert False
