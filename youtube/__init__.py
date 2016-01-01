from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from .yt import youtube_search, youtube_playlist
from model import GameRanking
from cache import cache

app = Blueprint('youtube', __name__)


@app.record
def record_params(setup_state):
    root = setup_state.app
    app.config = dict([(key, value) for (key, value) in root.config.items()])


###
# Routing for your application.
###
SEARCH_ARGS = {
    "q": str,
    "type": str,
    "part": str,
    "maxResults": int,
    "channelId": str,
    "location": str,
    "locationRadius": str,
    "order": str,
    "pageToken": str,
    "publishedAfter": datetime,
    "publishedBefore": datetime,
    "regionCode": str,
    "topicId": str,
    "videoCategoryId": str,
    "videoDefinition": str,
    "videoDimension": str,
    "videoDuration": str,
    "videoEmbeddable": str,
    "videoLicense": str,
    "videoSyndicated": str,
    "videoType": str
}


@app.route('/search', methods=["GET"])
def search():
    """Search the youtube and return the result."""
    kwargs = {
        "type": "video",
        "part": "id,snippet",
        "maxResults": 25,
        "order": "relevance"
    }
    for key, method in SEARCH_ARGS.items():
        value = request.args.get(key, None)
        if value:
            kwargs[key] = method(value)
    try:
        return jsonify(youtube_search(app.config["GOOGLE_CLIENT_KEY"], **kwargs))
    except:
        abort(500)


@app.route('/countries/<country>', methods=["GET"])
@cache.cached(timeout=3600 * 12)
def games(country):
    try:
        r = GameRanking.objects.get(country=country)
        games = set()
        for k, game_list in r.rank.items():
            for g in game_list[:8]:
                games.add(g.get("name"))
        items = []
        for g in games:
            items += youtube_search(app.config["GOOGLE_CLIENT_KEY"],
                                    q=g,
                                    type="video",
                                    part="id,snippet",
                                    maxResults=2,
                                    order="relevance",
                                    regionCode=r.code).get("items", [])
        return jsonify({"result": items})
    except Exception as e:
        print e
        abort(404)


@app.route('/playlist/<id>', methods=['POST'])
@cache.cached(timeout=3600)
def play_list(id):
    kwargs = {
        "pageToken": request.args.get("pageToken", None),
        "part": "id,snippet",
        "maxResults": int(request.args.get("maxResults", 20))
    }
    return jsonify(youtube_playlist(
        app.config["GOOGLE_CLIENT_KEY"],
        id,
        **kwargs
    ))
