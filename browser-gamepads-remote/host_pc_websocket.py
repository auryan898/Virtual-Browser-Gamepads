import asyncio
import websockets
import json
import time
from threading import Thread

from gamepad_driver import GamepadAssigner

DEBUG = False

async def gamepad_listening(assigner, uri, host_name, run_forever=-1):
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
    {"host_name": "ryan pc", "assignments": {"ryan": 3}}
    {"host_name": "ryan pc", "assignments": {"ryan": 3}}
    >>> time.sleep(5)
    '''
    
    is_start = True
    async with websockets.connect(uri) as websocket:
        while True:
            if run_forever == 0:
                break
            data = json.dumps({ 'host_name': host_name, 'assignments': assigner.vjoy_gamer_id })
            await websocket.send(data)

            resp = await websocket.recv()
            assigner.update_gamers_json(json.loads(resp))
            time.sleep(0.1)
            if run_forever > 0: # <0 for forever, >=0 for that many iterations
                run_forever -= 1


def main_ws():
    config = None
    with open('host_pc_config.json','r') as f:
        config = json.load(f)
        print(config)
    loop = asyncio.new_event_loop()
    assigner = GamepadAssigner.get_assigner()
    def f(loop, loop_data, assigner):
        asyncio.set_event_loop(loop)
        try:
            action = gamepad_listening(assigner, config['broker_uri'], config['host_name'])
            loop_data['is_running'] = True
            loop.run_until_complete(action) # 'ws://localhost:8765'
        except Exception as e:
            print(e)
        finally:
            loop_data['is_running'] = False
    loop_data = {'is_running' : False}
    t = Thread(target=f, args=(loop, loop_data, assigner))
    t.start()

    # Start Display with assigner
    display = AssignerDisplay(assigner, loop)
    while True:
        # Update display window
        if display.update_display(loop_data['is_running']):
            break
        time.sleep(0.1)
    # Closing of both loop and window
    try:
        loop.close() # close it, might fail, but that's okay
    except Exception:
        pass
    display.close_display()

import PySimpleGUI as sg
class AssignerDisplay(object):
    def __init__(self, assigner, loop):
        self.column = [
            [sg.Text("Loading...", size=(40,1), key="-STATUS-")],
            [sg.Listbox(
                values = [], enable_events=True, size=(40,20), key="-GAMERS-"
            )],
            [
                sg.Button("Refresh", key='-REFRESH-'), sg.Button("Reconnect", key='-RECONNECT-')
            ]
        ]
        self.layout = [
            [sg.Column(self.column)]
        ]
        self.window = sg.Window("Browser Gamepads PC Host", self.layout)
        self.assigner = assigner
        self.loop = loop

        self.status_code = 0 # 0 is loading, 1 is connected, 2 is disconnected
    def update_display(self, is_loop_running):
        event, values = self.window.read()

        # ---Perform Event-based Action---
        if event == '-REFRESH-':
            pass
        elif event == '-GAMERS-' and len(values['-GAMERS-'])>0:
            print(values)
            items = values['-GAMERS-'][0] # list
            if len(items) > 0 and type(items) == str:
                vals = items.split('|')
                print(vals)
                gamer_id = vals[0].strip()
                print(gamer_id)
                self.assigner.swap_vjoy_gamer(gamer_id)
        elif event == '-RECONNECT-':
            pass
        # ---Update Display Code---
        if is_loop_running and self.status_code != 1:
            self.window['-STATUS-'].update(value='Connected.')
        elif not is_loop_running and self.status_code != 2:
            self.window['-STATUS-'].update(value='WARNING: Disconnected. Please reconnect')

        # Update list
        print(self.assigner.vjoy_gamer_id)
        gamers_list = [ 
            gamer + ' | ' + ('none' if stick_num==0 else str(stick_num)) 
            for gamer, stick_num in self.assigner.vjoy_gamer_id.items()
            ]
        self.window['-GAMERS-'].update(gamers_list)
        

        return event == sg.WIN_CLOSED
    def close_display(self):
        self.window.close()

if __name__=='__main__':
    if DEBUG:
        import doctest
        doctest.testmod()
    # GamepadAssigner.get_assigner().vjoy_gamer_id['ryan'] = 0
    main_ws() # run host pc websocket client