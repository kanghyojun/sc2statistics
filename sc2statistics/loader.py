import logging
import os

from mpyq import MPQArchive
from s2protocol.versions import build, latest

from .exceptions import S2ProtocolNotFoundError


__all__ = 'load_all', 'load_protocol', 'load_replay'


def load_all(dir_):
    # FIXME use pathlib
    for root, _, fnames in os.walk(dir_):
        for name in fnames:
            if name.endswith('SC2Replay'):
                yield os.path.join(root, name)


def load_protocol(replay_name):
    """Get a replay decoder protocol.

    """
    archive = MPQArchive(replay_name)
    contents = archive.header['user_data_header']['content']
    latest_protocol = latest()
    header = latest_protocol.decode_replay_header(contents)
    build_version = header['m_version']['m_baseBuild']
    try:
        protocol = build(build_version)
    except ImportError:
        raise S2ProtocolNotFoundError(build_version)
    else:
        return archive, protocol


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
        logging.error('s2protocol(%s) not found.'
                      'check out version of s2protocol.', e.message)
        raise
    return {'tracker_events': tuple(r), 'details': detail}
