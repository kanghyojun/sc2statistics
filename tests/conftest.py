# -*- coding: utf-8 -*-
from contextlib import contextmanager
from pytest import fixture

from sc2statistics.loader import load_all, load_replay


@fixture
def f_replay_data():
    n = list(load_all('./tests/assets'))[0]
    return load_replay(n)


@fixture
@contextmanager
def f_replay():
    n = list(load_all('./tests/assets'))[0]
    with open(n, 'rb') as f:
        yield f
