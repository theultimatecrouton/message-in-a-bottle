from flask import Flask, jsonify, make_response, request, abort
import redis
import os
import socket
import pickle

# Connect to Redis
# r =  redis.StrictRedis(host='localhost', port=6379, db=0)
entries = []

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


@app.route('/message', methods=['GET'])
def get_message():
    # read and return message from db
    # TODO: need to handle empty db
    # key = r.randomkey()
    # return jsonify(pickle.loads(redis.get(key)))
    return jsonify(entries.pop()) if entries else jsonify({'message': 'no bottles!'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/message', methods=['POST'])
def write_message():
    if not request.json or not 'message' in request.json:
        abort(400)
    # add to db
    author, date = '', ''
    if 'author' in request.json:
        author = request.json['author']
    if 'date' in request.json:
        date = request.json['date']

    entry = {'message': request.json['message'],
             'author': author,
             'date': date}
    # r.set(str(hash(frozenset(entry))), pickle.dumps(entry))
    entries.append(entry)
    return jsonify(entry), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
