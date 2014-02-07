# -*- coding: utf-8 -*-
from functools import wraps

from .env import UNIT

__all__ ='get_build', 'get_unit', 'get_player', 'get_timeline',


S2_TIME_CORR_VAL = 1/16.0
TRACKER_BORN_EVENT = 'NNet.Replay.Tracker.SUnitBornEvent'
TRACKER_INIT_EVENT = 'NNet.Replay.Tracker.SUnitInitEvent'
TRACKER_DIED_EVENT = 'NNet.Replay.Tracker.SUnitDiedEvent'


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


@events('tracker', TRACKER_INIT_EVENT)
def get_build(replay_data, player_id=None):
    for v in replay_data:
        yield {'built_at': v['_gameloop'] * S2_TIME_CORR_VAL,
               'name': v['m_unitTypeName'],
               'player_id': v['m_controlPlayerId']}


@events('tracker', TRACKER_BORN_EVENT)
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


@events('tracker', TRACKER_INIT_EVENT, TRACKER_BORN_EVENT, TRACKER_DIED_EVENT)
def get_timeline(replay_data, player_id=None):
    tag_index = {}
    supply = [6 for x in xrange(8)]
    for event in replay_data:
        t = event['_gameloop'] * S2_TIME_CORR_VAL
        event_name = 'init'
        if event['_event'] == TRACKER_BORN_EVENT:
            player_id = event['m_controlPlayerId']
            unit_name = event['m_unitTypeName']
            unit = UNIT[event['m_unitTypeName']]
            t -= unit['build_time']
            if unit_name == 'Larva':
                continue
            tag_index[event['m_unitTagIndex']] = {
              'unit': unit, 'player_id': player_id, 'unit_name': unit_name
            }
            supply[player_id] += unit['supply']
        elif (event['_event'] == TRACKER_DIED_EVENT and
                event['m_unitTagIndex'] in tag_index):
            event_name = 'die'
            tagged = tag_index[event['m_unitTagIndex']]
            if tagged['unit_name'] == 'Zergling':
                supply[tagged['player_id']] -= 0.5
            elif tagged['unit_name'] == 'Larva':
                continue
            else:
                supply[tagged['player_id']] -= tagged['unit']['supply']
            event['m_unitTypeName'] = tagged['unit_name']
            event['m_controlPlayerId'] = tagged['player_id']
        elif event['_event'] == TRACKER_INIT_EVENT:
            pass
        else:
            continue
        yield {'started_at': t,
               'supply': int(supply[event['m_controlPlayerId']]),
               'thing': event['m_unitTypeName'], 'event': event_name,
               'player_id': event['m_controlPlayerId']}
