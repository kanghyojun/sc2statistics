# -*- coding: utf-8 -*-
from os import walk, path

from mpyq import MPQArchive
from s2protocol import protocol15405

from .exceptions import S2ProtocolNotFoundError
from .loging import get_logger

def load_all(dir_):
    for root, _, fnames in walk(dir_):
        for name in fnames:
            if name.endswith('SC2Replay'):
                yield path.join(root, name)


def load_protocol(replay_name):
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
    r = None
    try:
        archive, protocol = load_protocol(replay_name)
        contents = archive.read_file('replay.game.events')
        r = protocol.decode_replay_game_events(contents)
    except S2ProtocolNotFoundError as e:
        logger = get_logger()
        logger.error('s2protocol(%s) not found.'
                     'check out version of s2protocol.' % e.message)
    return r
