# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile

from flask import Flask, request, jsonify

from sc2statistics.loader import load_replay
from sc2statistics.game import get_build, get_player

from ..db import session, ensure_shutdown_session


app = Flask(__name__)


@app.route('/analyze_replays/', methods=['POST'])
def analyze_replay():
    replay_file = request.files.get('replay', None)
    replay_data = load_replay(replay_file)
    build = get_build(replay_data)
    player = get_player(replay_data)
    if replay_file is None:
        abort(400)
    return jsonify(build=list(build), player=player)

ensure_shutdown_session(app)
