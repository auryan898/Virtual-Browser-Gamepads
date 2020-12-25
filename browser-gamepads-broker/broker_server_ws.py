from flask import Flask, render_template
from flask_sockets import Sockets
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ryanIsSecret'
sockets = Sockets(app)

GAMEPAD_DATA = {} # Contains names of gamer IDs
ASSIGNMENTS = {}

@sockets.route('/hosts')
def handle_pc_host(ws): # { host_name: str, assigned_gamers}
    while not ws.closed:
        obj = json.loads(ws.receive())
        print('received json '+ str(obj))
        ws.send(generate_host_data(obj['assignments'], obj['host_name']))
        print('send json ' + str(generate_host_data(obj['assignments'])))

def generate_host_data(assignments, host_name) -> dict:
    '''(dict) -> dict
    Creates the gamepad data dict based on the given assignments, ex. {'ryan':1,'bob':0}, returned as 
    {'ryan':gamepad_data, 'bob':None}, only for assignments between [1,4] inclusive.
    '''
    result = {}
    for gamerID, stick_num in assignments.items():
        if stick_num >= 1 and stick_num <= 4 and gamerID in GAMEPAD_DATA:
            result[gamerID] = GAMEPAD_DATA[gamerID]
        ASSIGNMENTS[gamerID] = {'stick_num':stick_num, 'host_name':host_name}
    return json.dumps(result)

@sockets.route('/clients')
def handle_gamepad_client(ws):
    '''
    Expects a json of {gamepad: gamepadData, ID: gamerID}
    '''
    while not ws.closed:
        obj = json.loads(ws.receive())
        for key, data in obj['gamepad'].items():
            GAMEPAD_DATA[key] = data
        assignment = ASSIGNMENTS.get(obj['ID'], None)
        if assignment and 'stick_num' in assignment and 'host_name' in assignment:
            ws.send({'controller_assignment': assignment['stick_num'], 'connected_host': assignment['host_name']})

@app.route('/')
def hello():
    return 'Hello World!'

if __name__=='__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    print('Serving on port 5000')
    server.serve_forever()