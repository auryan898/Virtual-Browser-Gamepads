# Browser Gamepads

Browser gamepads is an quick project that allows you to use any device that can access the internet to connect to a Windows computer as a gamepad. There are other remote control solutions, however they are too clunky, and provide far too many features and complexity. This application specifically provides remote gamepads with just a set of buttons that send gamepad input signals to the remote PC.

## Project Organization

Host PC to add gamepads to, using the following gamepad emulation libraries:
- [PYXInput](https://pypi.org/project/PYXInput/)
- [PyDirectInput](https://pypi.org/project/PyDirectInput/)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [websockets](https://websockets.readthedocs.io/en/stable/)
- [pyvjoy](https://github.com/tidzo/pyvjoy)

Flask and Flask-SocketIO for the server.
- [Flask-Sockets]()
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [(deprecated) Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)

PhaserJS for the joystick client GUI, of remote gamepads.
- [PhaserJS](https://phaser.io/)
- [PhaserJS VirtualGamepad](https://github.com/ShawnHymel/phaser-plugin-virtual-gamepad)
- [Touch-enabled Virtual JoyStick](https://www.cssscript.com/touch-joystick-controller/)

VueJS for other logistical elements:
- [VueJS](https://vuejs.org/)

## Steps to Implementation

1. Implement a combined driver for adding, removing, managing, and viewing virtual gamepads.

2. Setup a host script that connects to a server and provides a socket based connection to manipulate the virtual gamepads

3. Implement a server that uses the virtual gamepad and provides a basic set of html buttons.

4. Implement a better gamepad client GUI to be served by the server.

## Final Steps for Implementation

1. Host Broker server on heroku, and also put up the client gamepad somewhere

2. Finish client gamepad UI and organization. Add name selector button, and possibly just a settings button

3. Create Host PC UI for choosing assignable players at the minimum

4. Remove hardcoded value of 'ryan' from everything, and make it dynamic. Use a short 6-code UID

5. (optional) Optimize client remote gamepad update loop (probably modulo something)

6. (optional) Add more than just the vjoy controller

7. (optional) Password protected gamepad and host access