# -*- coding: utf-8 -*-
from functools import wraps

__all__ ='get_build', 'get_unit', 'get_player', 'get_timeline',


S2_TIME_CORR_VAL = 1/1.6


def events(event_name, *events):
    def wrapper(f):
        @wraps(f)
        def deco(*args, **kwargs):
            d = args and args[0] or kwargs['replay_data']
            filtered = []
            player_id = kwargs.get('player_id', None)
            for item in d[event_name + '_events']:
                if (item['_event'] in events and player_id is None or
                        player_id == item.get('m_controlPlayerId', -1)):
                    if item['_gameloop'] != 0:
                        filtered.append(item)
            return f(replay_data=filtered)
        return deco
    return wrapper


@events('tracker', 'NNet.Replay.Tracker.SUnitInitEvent')
def get_build(replay_data, player_id=None):
    for v in replay_data:
        yield {'built_at': v['_gameloop'] * S2_TIME_CORR_VAL,
               'name': v['m_unitTypeName'],
               'player_id': v['m_controlPlayerId']}


@events('tracker', 'NNet.Replay.Tracker.SUnitBornEvent')
def get_unit(replay_data, player_id=None):
    for v in replay_data:
        yield {'born_at': v['_gameloop'] * S2_TIME_CORR_VAL,
               'name': v['m_unitTypeName'],
               'player_id': v['m_controlPlayerId']}


def get_player(replay_data):
    r = {}
    for item in replay_data['details']['m_playerList']:
        r[int(item['m_teamId']) + 1] = {
            'name': item['m_name'].replace('<sp/>', ' '),
            'race': item['m_race'],
            'color': item['m_color'],
        }
    return r


@events('tracker', 'NNet.Replay.Tracker.SUnitInitEvent,'
                   'NNet.Replay.Tracker.SUnitBornEvent,'
                   'NNet.Replay.Tracker.SUnitDieEvent')
def get_timeline(replay_data, player_id=None):
    return replay_data
