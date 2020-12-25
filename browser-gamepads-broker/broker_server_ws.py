from flask import Flask, render_template
from flask_sockets import Sockets
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ryanIsSecret'
sockets = Sockets(app)

GAMEPAD_DATA = {} # Contains names of gamer IDs

@sockets.route('/hosts')
def handle_pc_host(ws): # { host_name: str, assigned_gamers}
    while not ws.closed:
        obj = json.loads(ws.receive())
        print('received json '+ str(obj))
        ws.send(generate_host_data(obj['assignments']))
        print('send json ' + str(generate_host_data(obj['assignments'])))

def generate_host_data(assignments) -> dict:
    '''(dict) -> dict
    Creates the gamepad data dict based on the given assignments, ex. {'ryan':1,'bob':0}, returned as 
    {'ryan':gamepad_data, 'bob':None}, only for assignments between [1,4] inclusive.
    '''
    result = {}
    for key,value in assignments.items():
        if value >= 1 and value <= 4 and key in GAMEPAD_DATA:
            result[key] = GAMEPAD_DATA[key]
    return json.dumps(result)

@sockets.route('/clients')
def handle_gamepad_client(obj):
    print('received json:' + str(obj))

@app.route('/')
def hello():
    return 'Hello World!'

if __name__=='__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    print('Serving on port 5000')
    server.serve_forever()