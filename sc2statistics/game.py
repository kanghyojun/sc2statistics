# -*- coding: utf-8 -*-
from functools import wraps

__all__ ='get_build', 'get_unit'


S2_TIME_CORR_VAL = 1/1.6


def tracker_events(event):
    def wrapper(f):
        @wraps(f)
        def deco(*args, **kwargs):
            d = args and args[0] or kwargs['replay_data']
            filtered = []
            player_id = kwargs.get('player_id', None)
            for item in d['tracker_events']:
                if (item['_event'] == event and player_id is None or
                        player_id == item.get('m_controlPlayerId', -1)):
                    filtered.append(item)
            return f(replay_data=filtered)
        return deco
    return wrapper


@tracker_events('NNet.Replay.Tracker.SUnitInitEvent')
def get_build(replay_data, player_id=None):
    for v in replay_data:
        yield {'built_at': v['_gameloop'] * S2_TIME_CORR_VAL,
               'name': v['m_unitTypeName'],
               'player_id': v['m_controlPlayerId']}


@tracker_events('NNet.Replay.Tracker.SUnitBornEvent')
def get_unit(replay_data, player_id=None):
    for v in replay_data:
        yield {'born_at': v['_gameloop'] * S2_TIME_CORR_VAL,
               'name': v['m_unitTypeName'],
               'player_id': v['m_controlPlayerId']}
