# message-in-a-bottle
Read a message or send off a message in a bottle!

## Usage

### `GET /message`
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
