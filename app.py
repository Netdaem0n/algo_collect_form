import flask
from flask import request, jsonify, redirect, url_for, render_template

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home_main():
    return jsonify({'message': 'Test fo nginx proxy', 'status': request.access_route,
                    'headers': list(request.headers.items())})