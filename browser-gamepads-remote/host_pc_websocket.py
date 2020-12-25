import asyncio
import websockets
import socketio
import json

from gamepad_driver import GamepadAssigner

DEBUG = False

async def gamepad_listening(uri, host_name, run_forever=-1):
    '''
    >>> import asyncio, websockets, time, json
    >>> a = GamepadAssigner.get_assigner()
    >>> a.set_vjoy_gamer('ryan', 3)
    >>> async def hello(websocket, path):
    ...     resp = await websocket.recv()
    ...     print(resp)
    ...     await websocket.send(json.dumps({'ryan':{'lx':'32000'}, 'bob':{'ly':32000}}))
    ...     resp = await websocket.recv()
    ...     print(resp)
    ...     time.sleep(2)
    ...     await websocket.send(json.dumps({'ryan':{'lx':16384}, 'bob':{'ly':16384}}))
    >>> from concurrent.futures import ProcessPoolExecutor
    >>> executor = ProcessPoolExecutor(2)
    >>> loop = asyncio.get_event_loop()
    >>> tasks = [None, None]
    >>> tasks[1] = websockets.serve(hello, "localhost", 8765)
    >>> tasks[0] = gamepad_listening('ws://localhost:8765','ryan pc', 2)
    >>> _ = loop.run_until_complete(asyncio.wait(tasks))
    {"hostName": "ryan pc", "assignments": {"ryan": 3}}
    {"hostName": "ryan pc", "assignments": {"ryan": 3}}
    >>> time.sleep(5)
    '''
    
    is_start = True
    assigner = GamepadAssigner.get_assigner()
    async with websockets.connect(uri) as websocket:
        while True:
            if run_forever == 0:
                break
            data = json.dumps({ 'hostName': host_name, 'assignments': assigner.vjoy_gamer_id })
            await websocket.send(data)

            resp = await websocket.recv()
            assigner.update_gamers_json(json.loads(resp))

            if run_forever > 0: # <0 for forever, >=0 for that many iterations
                run_forever -= 1

def gamepad_listening_socketio(uri, host_name, run_forever=-1):
    ''''''
    assigner = GamepadAssigner.get_assigner()
    sio = socketio.Client()

    sio.connect(uri)
    @sio.on('json')
    def receive_gamepad_data(obj):
        assigner.update_gamers_json(obj)

    while True:
        if run_forever == 0:
            break
        sio.emit('json', { 
            'hostName': host_name, 
            'assignments': assigner.vjoy_gamer_id 
            })
        time.sleep(0.1)
        if run_forever > 0: # <0 for forever, >=0 for that many iterations
            run_forever -= 1

def main_socketio():
    config = None
    with open('host_pc_config.json','r') as f:
        config = json.load(f)
        print(config)
    gamepad_listening_socketio(config['broker_uri'], config['host_name'])

def main_ws():
    config = None
    with open('host_pc_config.json','r') as f:
        config = json.load(f)
        print(config)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(gamepad_listening(config['broker_uri'], config['host_name'])) # 'ws://localhost:8765'
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__=='__main__':
    if DEBUG:
        import doctest
        doctest.testmod()
    # main_socketio() 
    assigner = GamepadAssigner.get_assigner()
    assigner.set_vjoy_gamer('ryan',1)
    main_ws() # run host pc websocket client