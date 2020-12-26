# Virtual Browser Gamepads

Virtual Browser Gamepads allows you to use any web browser on any device that can access the internet to connect to a computer as a gamepad. There are other remote gamepad solutions, however they are too feature-heavy and complex for just the purposes of playing a game. This application specifically provides a remote gamepad UI on your phone that matches that of an Xbox One controller, or a PlayStation controller, with two joysticks, four buttons on the right, a directional pad, then two buttons for the left and right shoulders each.

## Installation

This project is currently a work in progress, and the dependencies are going to change, such as for supporting multiple platforms for the host PC (Windows, Linux, Mac).

There are three parts to this application, the "Server", the Host PC, and the remote gamepads in browser. 

- The Server communicates with the Host PC and remote gamepads, managing what information needs to go to whichever device
- Remote gamepads require no installation except navigating to a website url for each remote gamepad
- The Host PC runs a Python script that communicates with the Server, receiving inputs from selected remote gamepads, and then using that data on virtual gamepads on the Host PC

## Project Organization

Host PC to add gamepads to, using the following gamepad emulation libraries:
- [websockets](https://websockets.readthedocs.io/en/stable/)
- [pyvjoy](https://github.com/tidzo/pyvjoy)
- [PySDL2 (Cross-platform Focus)](https://pypi.org/project/PySDL2/)
- [PYXInput](https://pypi.org/project/PYXInput/)
- [PyDirectInput](https://pypi.org/project/PyDirectInput/)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)

Flask and Flask-SocketIO for the server.
- [Flask-Sockets](https://pypi.org/project/Flask-Sockets/)
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

0. Change entire setup to event based instead of polling based (Client-side DONE, Host unfinished) 50%

1. Create Host PC UI for choosing assignable players at the minimum (Bare minimum DONE)

2. Remove hardcoded value of 'ryan' from everything, and make it dynamic (DONE). Use a short 6-code UID (UNDONE)

3. --> Host Broker server on heroku, and also put up the client gamepad somewhere

4. --> Finish client gamepad UI and organization. Add name selector button, and possibly just a settings button

5. (optional) Optimize client remote gamepad update loop (probably modulo something) (Mostly Done)

6. (optional) Add more than just the vjoy controller (Should use SDL2, for cross-platform as well)

7. (optional) Password protected gamepad and host access