from flask import Blueprint, request, jsonify, abort

from model import GameRanking

app = Blueprint('appannie', __name__)

CODES = {
    "united-states": "US",
    "russia": "RU",
    "canada": "CA",
    "brazil": "BR",
    "south-korea": "KR",
    "japan": "JP",
    "spain": "ES",
}


@app.record
def record_params(setup_state):
    root = setup_state.app
    app.config = dict([(key, value) for (key, value) in root.config.items()])


@app.route('/<country>', methods=["POST"])
def update(country):
    """Update game list."""
    code = CODES.get(country, None)
    if code is None:
        return abort(404)
    try:
        GameRanking.objects(country=country, code=code).upsert_one(rank=request.get_json(force=True))
        return jsonify({"code": 0, "message": "ok"})
    except:
        abort(500)


@app.route('/countries/<country>', methods=["GET"])
def get(country):
    """Get game rank."""
    try:
        r = GameRanking.objects.get(country=country)
        return jsonify({"country": r.country, "rank": r.rank})
    except:
        abort(500)


@app.route('/countries', methods=["GET"])
def countries():
    try:
        return jsonify({"countries": GameRanking.objects.distinct("country")})
    except:
        abort(500)
