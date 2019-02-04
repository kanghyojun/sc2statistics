import datetime
import uuid

from sqlalchemy.schema import Column
from sqlalchemy.types import Unicode, UnicodeText

from .db import Base


def ordered_hash(length=20):
    epoch = datetime.datetime.utcfromtimestamp(0)
    now = datetime.datetime.now()
    seconds = hex((now - epoch).total_seconds())[2:]
    random_string = uuid.uuid4().hex
    random_string_len = length - len(seconds)
    return seconds + random_string[random_string_len:]


class Replay(Base):

    __tablename__ = 'replays'

    # FIXME The type of id need to be changed to `Binary`.
    id = Column(Unicode, primary_key=True, default=ordered_hash)

    build = Column(UnicodeText, nullable=False)

    unit = Column(UnicodeText, nullable=False)

    player = Column(UnicodeText, nullable=False)
