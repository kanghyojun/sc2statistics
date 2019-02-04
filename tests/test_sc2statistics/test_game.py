from sc2statistics.game import get_build, get_unit, get_player, get_timeline


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


def test_get_player(f_replay_data):
    player = get_player(f_replay_data)
    assert player
    assert 'name' in player[1]
    assert 'race' in player[1]
    assert 'color' in player[1]


def test_timeline(f_replay_data2):
    timeline = get_timeline(f_replay_data2)
    assert timeline
    print(timeline)
    for x in timeline:
        if x['player_id'] == 1:
            print(x)
    assert False
