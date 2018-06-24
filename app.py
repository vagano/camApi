from flask import Flask, g, jsonify
from ptzcam import PtzCam

app = Flask(__name__)


def _get_camera():
    cam = getattr(g, '_cam', None)
    if cam is None:
        cam = g._cam = PtzCam('192.168.1.110', 8999, 'admin', '', '/home/pi/camApi/venv/wsdl/')
    return cam


def _get_presets():
    presets = getattr(g, '_presets', None)
    if presets is None:
        cam = _get_camera()
        presets = g._presets = jsonify(cam.get_presets())
    return presets


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/cam/')
def hello_world2():
    return 'Hello World from Cam!'


if __name__ == '__main__':
    app.run()
