from flask import Flask, jsonify, make_response, request, abort
import redis
import os
import socket
import pickle
import datetime

# Connect to Redis
r =  redis.StrictRedis(host='redis', port=6379, db=0)

app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h3>Welcome to message in a bottle</h3>" \
           "<b>Refer to https://github.com/theultimatecrouton/message-in-a-bottle for API usage<br/>"
    return html


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
    if not request.json or not 'message' in request.json:
        abort(400)
    # add to db
    author, location = '', ''
    if 'author' in request.json:
        author = request.json['author']
    if 'location' in request.json:
        location = request.json['location']

    date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    entry = {'message': request.json['message'],
             'author': author,
             'date': date,
             'location': location}
    r.set(str(hash(frozenset(entry))), pickle.dumps(entry))
    return jsonify(entry), 201

@app.route('/counter')
def message_count():
    return jsonify({'message count': len(r.keys())})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
