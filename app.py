import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, jsonify
from ptzcam import PtzCam

app = Flask(__name__)


def _get_camera():
    try:
        cam = getattr(g, '_cam', None)
        if cam is None:
            cam = g._cam = PtzCam('192.168.1.110', 8999, 'admin', '', '/home/pi/camApi/venv/wsdl/')
        return cam
    except Exception as e:
        app.logger.error(str(e))
        return '500'


def _get_presets():
    try:
        presets = getattr(g, '_presets', None)
        if presets is None:
            cam = _get_camera()
            presets = g._presets = jsonify(cam.get_presets())
        return presets
    except Exception as e:
        app.logger.error(str(e))
        return '500'


@app.route('/cam/api/get_presets_list/')
def get_presets_list():
    presets = _get_presets()
    return presets


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()
