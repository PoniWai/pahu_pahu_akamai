import ujson


class Settings:
    file_name = 'settings.json'

    def __init__(self,
                 wifi_dict,
                 onewire_dict,
                 loads_dict,
                 ):
        self.wifi_dict = wifi_dict
        self.onewire_dict = onewire_dict
        self.loads_dict = loads_dict

    @staticmethod
    def get_default_settings():
        wifi_dict = {
            'ap_ssid': 'HUJAWEI-STN29A',
            'ap_password': 'administrad0R',
            'ap_channel': 7,
            'sta_dict': {'SzpielP': 'Peezda345!?,.', 'Gdanska146': '60021045'}
        }
        onewire_dict = {
            'air': None,
            'space': None,
        }
        loads_dict = {
            'cool_top': 'checked',
            'cool_brd': 'checked',
            'cool_spc': 'checked',
            'light': 'checked',
        }

        return Settings(wifi_dict,
                        onewire_dict,
                        loads_dict,
                        )

    def save_settings(self):
        settings_json = ujson.dumps(self.__dict__)
        try:
            f = open(Settings.file_name, 'w')
            f.write(settings_json)
            f.close()
            return True
        except:
            return False

    @staticmethod
    def load_settings():
        try:
            f = open(Settings.file_name, 'r')
            settings_string = f.read()
            f.close()
            settings = ujson.loads(settings_string)
            result = Settings.get_default_settings()
            for setting in settings:
                setattr(result, setting, settings[setting])
            return result
        except:
            print('Settings file load failed')
            return Settings.get_default_settings()

    @staticmethod
    def clear_settings():
        f = open(Settings.file_name, 'w')
        f.write('')
        f.close()
