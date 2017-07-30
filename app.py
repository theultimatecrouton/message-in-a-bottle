from flask import Flask, jsonify, make_response, request, abort, render_template, \
 redirect, url_for
from werkzeug.exceptions import BadRequest
import redis
import os
import socket
import pickle
import datetime
import random


# Connect to Redis
r =  redis.StrictRedis(host='redis', port=6379, db=0)

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/message', methods=['GET'])
def get_message():
    # read and return message from db
    key = r.randomkey()
    serialised_entry = r.get(key)

    if serialised_entry:
        r.delete(key)
        return jsonify(pickle.loads(serialised_entry))
    return jsonify({'message': 'no bottles!'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/message', methods=['POST'])
def write_message():
    if request.json:
        request_to_use = request.json
    elif request.form:
        request_to_use = request.form
    else:
        abort(400)
    if not 'message' in request_to_use:
        abort(400)

    # add to db
    message = request_to_use['message']
    author, location = '', ''
    if 'author' in request_to_use:
        author = request_to_use['author']
    if 'location' in request_to_use:
        location = request_to_use['location']

    date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    entry = {'message': message,
             'author': author,
             'date': date,
             'location': location}
    r.set(date + str(random.random())[:4], pickle.dumps(entry))
    return jsonify(entry), 201


@app.route('/counter', methods=['GET'])
def message_count():
    return jsonify({'message count': len(r.keys())})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
