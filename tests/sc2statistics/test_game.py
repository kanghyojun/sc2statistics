# -*- coding: utf-8 -*-
from sc2statistics.game import get_build, get_unit


def test_get_build(f_replay_data):
    build = list(get_build(f_replay_data))
    assert build
    build_by_player1 = list(get_build(f_replay_data, player_id=1))
    assert build_by_player1
    for item in build_by_player1:
        assert 1 == item['player_id']


def test_get_unit(f_replay_data):
    unit = list(get_unit(f_replay_data))
    assert unit
    unit_by_player1 = list(get_unit(f_replay_data, player_id=1))
    assert unit_by_player1
    for item in unit_by_player1:
        assert 1 == item['player_id']
