# message-in-a-bottle
Read a message or send off a message in a bottle!

## Usage

### `GET /message`
Returns a random message from a bottle. These are read once before being gone forever so make the most of it...

e.g. `curl -i http://host/message`

Returns JSON:
```
{
  "author": "Tom",
  "date": "2017-07-26 21:03:49",
  "location": "London",
  "message": "Greetings from London"
}
```

### `POST /message`
Put a message in a bottle and send it away...

Expects JSON with at least the "message" field. Can also populate "location" and "author".

e.g. `curl -H "Content-Type: application/json" -X POST -d '{"message":"Why would you burn... the rum", "author":"Jack Sparrow", "location":"Tortuga"}' http://host/message`

### `GET /counter`
Returns the number of messages currently out on the seas
