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
    rp2 = f_session.query(Replay)\
          .filter(Replay.id == rp.id)\
          .first()
    assert rp2
    assert rp.id == rp2.id
    assert rp.build == rp2.build
    assert rp.unit == rp2.unit


def test_replay_primary_key(f_session):
    rp = Replay(build=u'a', unit=u'a')
    rp2 = Replay(build=u'a', unit=u'a')
    f_session.add(rp)
    f_session.add(rp2)
    f_session.commit()
    assert rp.id
    assert rp2.id
    # have to be unique
    assert rp.id != rp2.id
