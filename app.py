#!/usr/bin/env python
import os
from flask import Flask, jsonify

app = Flask(__name__)
app.config['GOOGLE_CLIENT_KEY'] = os.environ.get("GOOGLE_CLIENT_KEY", "AIzaSyAl47M1QiibtSXtq1QbdEsVEUa-0zeW028")

from youtube import app as youtube_app
app.register_blueprint(youtube_app, url_prefix='/youtube')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def not_found(error):
    """Custom 404 json."""
    response = jsonify({'code': 404, 'message': 'No interface defined for URL'})
    response.status_code = 404
    return response


@app.errorhandler(500)
def server_error(error):
    """Custom 500 json."""
    response = jsonify({'code': 500, 'message': 'Internal server error!'})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(debug=True)
