import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, jsonify
from ptzcam import PtzCam
from flask_cors import CORS

import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/cam/api/*": {"origins": "*"}})


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


@app.route('/cam/api/get_presets_list/')
def get_presets_list():

    if not os.path.isfile('/home/pi/camApi/presets.json'):
        presets = _get_presets()
        presets_json = {}


        with open('/home/pi/camApi/presets_dict.json', 'r') as jsondictfile:
            presets_dict = json.load(jsondictfile)

        try:
            for p in presets:
                token = str(p._token)
                token_name = str(p.Name)
                presets_json[token] = {
                    "token_name": token_name,
                    "name_ru": presets_dict[token_name]['ru'],
                    "name_en": presets_dict[token_name]['en']
                }
        except Exception as e:
            pass

        try:
            with open('/home/pi/camApi/presets.json', 'w') as jsonfile:
                json.dump(presets_json, jsonfile)
        except Exception as e:
            return str(e)
    else:
        with open('/home/pi/camApi/presets.json', 'r') as jsonfile:
            presets_json = json.load(jsonfile)

    return jsonify(presets_json)


@app.route('/cam/api/move_to_preset/<int:token>')
def move_to_preset(token):
    try:
        cam = _get_camera()
        cam.goto_preset(token)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


if __name__ == '__main__':
    handler = RotatingFileHandler('/home/pi/camApi/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.logger.info('file was written')
    app.run()
