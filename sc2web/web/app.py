import itertools
import json

from flask import Flask, abort, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from ..db import ensure_shutdown_session, session
from ..replay import Replay
from sc2statistics.game import get_build, get_player, get_unit
from sc2statistics.loader import load_replay


__all__ = 'app',
app = Flask(__name__)


@app.route('/analyze_replays/', methods=['POST'])
def analyze_replays():
    replay_file = request.files.get('replay', None)
    if replay_file is None:
        abort(400)
    replay_data = load_replay(replay_file)
    if not replay_data:
        abort(400)
    build = get_build(replay_data)
    player = get_player(replay_data)
    unit = get_unit(replay_data)
    if not build or not player or not unit:
        abort(400)
    replay = Replay(build=json.dumps(list(build)),
                    player=json.dumps(player),
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
def get_analyzed_replay(replay_id):
    replay = session.query(Replay)\
             .filter(Replay.id == replay_id)\
             .first()
    if not replay:
        abort(404)
    try:
        # FIXME Change the type.
        build = json.loads(replay.build)
        player = json.loads(replay.player)
    except (ValueError, TypeError):
        abort(500)

    def find_player_id(item):
        return item['player_id']

    build_by_player = itertools.groupby(sorted(build, key=find_player_id),
                                        key=find_player_id)
    return render_template('view_build.html',
                           player=player, build=build_by_player)


# FIXME
ensure_shutdown_session(app)
