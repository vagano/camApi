#!/usr/bin/python

from onvif import ONVIFCamera
from time import sleep


class ptzcam():
    def __init__(self):
        print 'IP camera initialization'

        # Several cameras that have been tried  -------------------------------------
        # Netcat camera (on my local network) Port 8899
        self.mycam = ONVIFCamera('192.168.1.110', 8999, 'admin', '', '/home/pi/.local/wsdl/')
        # This is a demo camera that anyone can use for testing
        # Toshiba IKS-WP816R
        # self.mycam = ONVIFCamera('67.137.21.190', 80, 'toshiba', 'security', '/etc/onvif/wsdl/')

        print 'Connected to ONVIF camera'
        # Create media service object
        self.media = self.mycam.create_media_service()
        print 'Created media service object'
        print
        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]
        # Use the first profile and Profiles have at least one
        token = self.media_profile._token

        # PTZ controls  -------------------------------------------------------------
        print
        # Create ptz service object
        print 'Creating PTZ object'
        self.ptz = self.mycam.create_ptz_service()
        print 'Created PTZ service object'
        print

        # Get available PTZ services
        request = self.ptz.create_type('GetServiceCapabilities')
        Service_Capabilities = self.ptz.GetServiceCapabilities(request)
        print 'PTZ service capabilities:'
        print Service_Capabilities
        print

        # Get PTZ status
        status = self.ptz.GetStatus({'ProfileToken': token})
        print 'PTZ status:'
        print status
        print 'Pan position:', status.Position.PanTilt._x
        print 'Tilt position:', status.Position.PanTilt._y
        print 'Zoom position:', status.Position.Zoom._x
        print 'Pan/Tilt Moving?:', status.MoveStatus.PanTilt
        print

        # Get PTZ configuration options for getting option ranges
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration._token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)
        print 'PTZ configuration options:'
        print ptz_configuration_options
        print

        self.requestc = self.ptz.create_type('ContinuousMove')
        self.requestc.ProfileToken = self.media_profile._token

        self.requesta = self.ptz.create_type('AbsoluteMove')
        self.requesta.ProfileToken = self.media_profile._token
        print 'Absolute move options'
        print self.requesta
        print

        self.requestr = self.ptz.create_type('RelativeMove')
        self.requestr.ProfileToken = self.media_profile._token
        print 'Relative move options'
        print self.requestr
        print

        self.requests = self.ptz.create_type('Stop')
        self.requests.ProfileToken = self.media_profile._token

        self.requestp = self.ptz.create_type('SetPreset')
        self.requestp.ProfileToken = self.media_profile._token

        self.requestg = self.ptz.create_type('GotoPreset')
        self.requestg.ProfileToken = self.media_profile._token

        print 'Initial PTZ stop'
        print
        self.stop()

    # Stop pan, tilt and zoom
    def stop(self):
        self.requests.PanTilt = True
        self.requests.Zoom = True
        print 'Stop:'
        # print self.requests
        print
        self.ptz.Stop(self.requests)
        print 'Stopped'

    # Continuous move functions
    def perform_move(self, timeout):
        # Start continuous move
        ret = self.ptz.ContinuousMove(self.requestc)
        print 'Continuous move completed', ret
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.stop()
        sleep(2)
        print

    def move_tilt(self, velocity, timeout):
        print 'Move tilt...', velocity
        self.requestc.Velocity.PanTilt._x = 0.0
        self.requestc.Velocity.PanTilt._y = velocity
        self.perform_move(timeout)

    def move_pan(self, velocity, timeout):
        print 'Move pan...', velocity
        self.requestc.Velocity.PanTilt._x = velocity
        self.requestc.Velocity.PanTilt._y = 0.0
        self.perform_move(timeout)

    def zoom(self, velocity, timeout):
        print 'Zoom...', velocity
        self.requestc.Velocity.Zoom._x = velocity
        self.perform_move(timeout)

    # Absolute move functions --NO ERRORS BUT CAMERA DOES NOT MOVE
    def move_abspantilt(self, pan, tilt, velocity):
        self.requesta.Position.PanTilt._x = pan
        self.requesta.Position.PanTilt._y = tilt
        self.requesta.Speed.PanTilt._x = velocity
        self.requesta.Speed.PanTilt._y = velocity
        print 'Absolute move to:', self.requesta.Position
        print 'Absolute speed:', self.requesta.Speed
        ret = self.ptz.AbsoluteMove(self.requesta)
        print 'Absolute move pan-tilt requested:', pan, tilt, velocity
        sleep(2.0)
        print 'Absolute move completed', ret

        print

    # Relative move functions --NO ERRORS BUT CAMERA DOES NOT MOVE
    def move_relative(self, pan, tilt, velocity):
        self.requestr.Translation.PanTilt._x = pan
        self.requestr.Translation.PanTilt._y = tilt
        self.requestr.Speed.PanTilt._x = velocity
        ret = self.requestr.Speed.PanTilt._y = velocity
        self.ptz.RelativeMove(self.requestr)
        print 'Relative move pan-tilt', pan, tilt, velocity
        sleep(2.0)
        print 'Relative move completed', ret
        print

    # Sets preset set, query and and go to
    def set_preset(self, name):
        self.requestp.PresetName = name
        self.requestp.PresetToken = '1'
        self.preset = self.ptz.SetPreset(self.requestp)  # returns the PresetToken
        print 'Set Preset:'
        print self.preset
        print

    def get_presets(self):
        self.ptzPresetsList = self.ptz.GetPresets(self.requestc)
        print 'Got preset:'
        print self.ptzPresetsList[0]
        print

    def goto_preset(self, name):
        self.requestg.PresetToken = '1'
        self.ptz.GotoPreset(self.requestg)
        print 'Going to Preset:'
        print name
        print

# -------------------------------------------------------------------------------
# Test of Python and Quatanium Python-ONVIF with NETCAT camera PT-PTZ2087
# ONVIF Client implementation is in Python
# For IP control of PTZ, the camera should be compliant with ONVIF Profile S
# The PTZ2087 reports it is ONVIF 2.04 but is actually 2.4 (Netcat said text not changed after upgrade)
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    # Do all setup initializations
    ptz = ptzcam()

    # *****************************************************************************
    # IP camera motion tests
    # *****************************************************************************
    print 'Starting tests...'

    # Set preset
    ptz.move_pan(1.0, 1)  # move to a new home position
    ptz.set_preset('home')

    # move right -- (velocity, duration of move)
    ptz.move_pan(1.0, 2)

    # move left
    ptz.move_pan(-1.0, 2)

    # move down
    ptz.move_tilt(-1.0, 2)

    # Move up
    ptz.move_tilt(1.0, 2)

    # zoom in
    ptz.zoom(8.0, 2)

    # zoom out
    ptz.zoom(-8.0, 2)

    # Absolute pan-tilt (pan position, tilt position, velocity)
    # DOES NOT RESULT IN CAMERA MOVEMENT
    ptz.move_abspantilt(-1.0, 1.0, 1.0)
    ptz.move_abspantilt(1.0, -1.0, 1.0)

    # Relative move (pan increment, tilt increment, velocity)
    # DOES NOT RESULT IN CAMERA MOVEMENT
    ptz.move_relative(0.5, 0.5, 8.0)

    # Get presets
    ptz.get_preset()
    # Go back to preset
    ptz.goto_preset('home')

    exit()

# *****************************************************************************
# IP Camera control
# Control methods:
#   rtsp video streaming via OpenCV for frame capture
#   ONVIF for PTZ control
#   ONVIF for setup selections
#
# Starting point for this code was from:
# https://github.com/quatanium/python-onvif
# *****************************************************************************

# import sys

# sys.path.append('/usr/local/lib/python2.7/dist-packages/onvif')

