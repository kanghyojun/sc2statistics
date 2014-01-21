# -*- coding: utf-8 -*-
from sc2statistics.loader import load_all, load_replay


def test_load_dir():
    r = list(load_all('./tests/assets'))
    assert r
    for n in r:
        assert n.endswith('SC2Replay')


def test_load_replay():
    for name in load_all('./tests/assets'):
        r = load_replay(name)
        assert 'tracker_events' in r
        assert 'details' in r
