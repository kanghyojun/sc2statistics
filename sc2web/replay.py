# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import uuid4

from sqlalchemy.types import TypeDecorator, Unicode, UnicodeText, Integer
from sqlalchemy.schema import Column

from .db import Base


def ordered_hash(length=20):
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    seconds = '%x' % (now - epoch).total_seconds()
    random_string = uuid4().hex
    random_string_len = length - len(seconds)
    postfix = random_string[random_string_len:]
    id_ = seconds + postfix
    return id_


class Replay(Base):

    __tablename__ = 'replays'

    id = Column(Unicode, primary_key=True, default=ordered_hash())

    build = Column(UnicodeText, nullable=False)

    unit = Column(UnicodeText, nullable=False)
