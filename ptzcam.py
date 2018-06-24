from onvif import ONVIFCamera


class PtzCam():
    def __init__(self,host,port,user,password,wsdl):
        self.mycam = ONVIFCamera(host, port, user, password, wsdl)
        self.media = self.mycam.create_media_service()
        self.media_profile = self.media.GetProfiles()[0]
        self.ptz = self.mycam.create_ptz_service()

        self.requestc = self.ptz.create_type('ContinuousMove')
        self.requestc.ProfileToken = self.media_profile._token

        self.requestg = self.ptz.create_type('GotoPreset')
        self.requestg.ProfileToken = self.media_profile._token

    def get_presets(self):
        self.ptzPresetsList = self.ptz.GetPresets(self.requestc)
        return self.ptzPresetsList

    def goto_preset(self, preset_token):
        self.requestg.PresetToken = preset_token
        self.ptz.GotoPreset(self.requestg)
