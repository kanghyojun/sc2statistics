# -*- coding: utf-8 -*-
from flask import json

from sc2web.web.app import app
from sc2web.replay import Replay

from .util import url_for


def test_replay_model(f_session):
    rp = Replay(build=u'a', unit=u'a')
    f_session.add(rp)
    f_session.commit()
    assert rp.id
    print rp.id
    assert False
