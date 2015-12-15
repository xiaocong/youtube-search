from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from .yt import youtube_search

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
