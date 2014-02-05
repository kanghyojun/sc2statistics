# -*- coding: utf-8 -*-
from flask import (Flask, request, jsonify, render_template, redirect,
                   url_for, json)
from sqlalchemy.exc import IntegrityError

from sc2statistics.loader import load_replay
from sc2statistics.game import get_build, get_player, get_unit

from ..db import session, ensure_shutdown_session
from ..replay import Replay


app = Flask(__name__)


@app.route('/analyze_replays/', methods=['POST'])
def analyze_replays():
    replay_file = request.files.get('replay', None)
    if replay_file is None:
        abort(400)
    replay_data = load_replay(replay_file)
    build = get_build(replay_data)
    player = get_player(replay_data)
    unit = get_unit(replay_data)
    replay = Replay(build=json.dumps(list(build)),
                    player=json.dumps(list(player)),
                    unit=json.dumps(list(unit)))
    session.add(replay)
    try:
        session.commit()
    except IntegrityError:
        abort(500)
    return redirect(url_for('get_analyzed_replay', replay_id=replay.id))


@app.route('/analyze_replays/', methods=['GET'])
def replays():
    return render_template('replay.html')


@app.route('/analyze_replays/<string:replay_id>/', methods=['GET'])
def get_analyzed_replay():
    return ''


ensure_shutdown_session(app)
