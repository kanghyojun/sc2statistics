# -*- coding: utf-8 -*-
from os import walk, path

from mpyq import MPQArchive
from s2protocol import protocol15405

from .exceptions import S2ProtocolNotFoundError
from .loging import get_logger


__all__ = 'load_all', 'load_protocol', 'load_replay',

def load_all(dir_):
    for root, _, fnames in walk(dir_):
        for name in fnames:
            if name.endswith('SC2Replay'):
                yield path.join(root, name)


def load_protocol(replay_name):
    """Get a replay decoder protocol.
    """
    archive = MPQArchive(replay_name)
    contents = archive.header['user_data_header']['content']
    header = protocol15405.decode_replay_header(contents)
    baseBuild = header['m_version']['m_baseBuild']
    protocol_name = 'protocol%s' % baseBuild
    try:
        protocol = __import__('s2protocol.%s' % protocol_name)
    except:
        raise S2ProtocolNotFoundError(protocol_name)
    return archive, getattr(protocol, protocol_name)


def load_replay(replay_name):
    """Get a replay datas.

    .. sourcecode::python

       >>> load_replay('hello.SC2Replay')
       {'tracker_events': {...}, 'details': {...}}
       >>> data = _
       >>> print data['details'][0]
       {'m_teamId': 0, 'm_name': 'Admire', 'm_race': 'Zerg', ...}
       >>> print data['tracker_events'][30]
       {'_event': 'NNet.Replay.Tracker.SUnitBornEvent', '_gameloop': 229,
       'm_unitTypeName': 'Drone', 'm_controlPlayerId': 0, ...}


    :return: return a dictionary has `tracker_events`, `details`.
             `tracker_events` is a events that shows when a unit was born
             (`NNet.Replay.Tracker.SUnitBornEvent`), when a struture made
             (`NNet.Replay.Tracker.SUnitInitEvent`).
             `details` explain about players and etc.
    """
    r = None
    try:
        archive, protocol = load_protocol(replay_name)
        contents = archive.read_file('replay.tracker.events')
        r = protocol.decode_replay_tracker_events(contents)
        contents = archive.read_file('replay.details')
        detail = protocol.decode_replay_details(contents)
#         contents = archive.read_file('replay.game.events')
#         game_events = protocol.decode_replay_game_events(contents)
    except S2ProtocolNotFoundError as e:
        logger = get_logger()
        logger.error('s2protocol(%s) not found.'
                     'check out version of s2protocol.' % e.message)
        raise
    return {'tracker_events': tuple(r), 'details': detail}
