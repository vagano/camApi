from flask import Flask, g
from ptzcam import PtzCam

app = Flask(__name__)


def _get_camera():
    cam = getattr(g, '_cam', None)
    if cam is None:
        cam = g._cam = PtzCam('192.168.1.110', 8999, 'admin', '', '/home/pi/.local/wsdl/')
    return cam


@app.route('/')
def hello_world():
    mycam = ONVIFCamera('85.12.222.142', 8999, 'admin', '', '/Users/vagano/PycharmProjects/camApi/venv/wsdl')
    # Create ptz service
    ptz_service = mycam.create_ptz_service()
    # Get ptz configuration
    # mycam.ptz.GetConfiguration()
    print(ptz_service.GetConfiguration())
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
