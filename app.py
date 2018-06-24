import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, jsonify
from ptzcam import PtzCam

from flask_debugtoolbar import DebugToolbarExtension

import socket
socket.setdefaulttimeout(3000)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'slkdjhfkjsdfjkdljaslkgfksalvdshjdk'

toolbar = DebugToolbarExtension(app)


def _get_camera():
    try:
        cam = getattr(g, '_cam', None)
        if cam is None:
            cam = g._cam = PtzCam('192.168.1.110', 8999, 'admin', '', '/home/pi/camApi/venv/wsdl/')
            # cam = g._cam = PtzCam('85.12.222.142', 8999, 'admin', '', '/Users/vagano/PycharmProjects/camApi/venv/wsdl/')
        return cam
    except Exception as e:
        app.logger.error(str(e))


def _get_presets():
    try:
        presets = getattr(g, '_presets', None)
        if presets is None:
            cam = _get_camera()
            presets = g._presets = cam.get_presets()
        return presets
    except Exception as e:
        app.logger.error(str(e))
        return e


@app.route('/cam/api/get_presets_list/')
def get_presets_list():
    presets = _get_presets()
    for p in presets:
        print (str(p._token), '-', str(p.name))
    return str(presets)


if __name__ == '__main__':
    handler = RotatingFileHandler('/home/pi/camApi/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()
