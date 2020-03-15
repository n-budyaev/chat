from flask import Flask, request
from datetime import datetime
import time


app = Flask(__name__)
messages = [
    {'username': 'Jack', 'text': 'Hello', 'time': time.time()},
    {'username': 'Mary', 'text': 'Hello, Jack', 'time': time.time()}
]
users = {
    #username: password
    'Jack': 'black',
    'Mary': '12345'
}

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/status")
def status():
    return {
     'status': True,
     'time': datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
     'user_count': len(users),
     'message_count': len(messages)
    }

@app.route("/history")
def history():
    """
    request: ?after=2246876878.3456
    response: {
        "messages": [
            {"username": "str", "text": "str", "time": float},
            ..."
        ]
    }
    """
    after = float(request.args['after'])

    # filtered_messages = []
    # for message in messages:
    #     if after < message['time']:
    #         filtered_messages.append(message)
    filtered_messages = [m for m in messages if after < m['time']]
    return {'messages': filtered_messages}


@app.route("/send", methods=['POST'])
def send():
    """
    request: {"username": "str", "password": "str", "text": "str"}
    response: {"ok": true}
    """
    data = request.json
    username = data['username']
    password = data['password']
    text = data['text']

    if username in users:
        real_password = users[username]
        if real_password != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'time': time.time()})

    return {'ok': True}

app.run()