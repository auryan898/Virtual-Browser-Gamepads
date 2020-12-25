from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ryanIsSecret'
socketio = SocketIO(app, namespaces=['/hosts'])

GAMEPAD_DATA = {} # Contains names of gamer IDs

@socketio.on('json', namespace='/hosts')
def handle_gamepad_client(obj): # { host_name: str, assigned_gamers}
    send(generate_host_data(obj['assignments']))
    print('received json '+ str(obj))
    print('send json ' + str(generate_host_data(obj['assignments'])))

def generate_host_data(assignments) -> dict:
    '''(dict) -> dict
    Creates the gamepad data dict based on the given assignments, ex. {'ryan':1,'bob':0}, returned as 
    {'ryan':gamepad_data, 'bob':None}, only for assignments between [1,4] inclusive.
    '''
    result = {}
    for key,value in assignments:
        if value >= 1 and value <= 4 and key in GAMEPAD_DATA:
            result[key] = GAMEPAD_DATA[key]
    return json.dumps(result)

@socketio.on('json', namespace='/clients')
def handle_pc_host(obj):
    print('received json:' + str(obj))


if __name__=='__main__':
    socketio.run(app)