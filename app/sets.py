import ujson


class Settings:
    file_name = 'settings.json'

    def __init__(self,
                 wifi_dict,
                 solution_dict,
                 air_dict,
                 power_dict,
                 light_dict,
                 onewire_dict,
                 anal_dict,
                 sensors_dict,
                 ):
        self.wifi_dict = wifi_dict
        self.solution_dict = solution_dict
        self.air_dict = air_dict
        self.power_dict = power_dict
        self.light_dict = light_dict
        self.onewire_dict = onewire_dict
        self.anal_dict = anal_dict
        self.sensors_dict = sensors_dict

    @staticmethod
    def get_default_settings():
        wifi_dict = {
            'ap_ssid': 'HUJAWEI-STN29A',
            'ap_password': 'administrad0R',
            'ap_channel': 7,
            'sta_dict': {'SzpielP': 'Peezda345!?,.',
            'Gdanska146': '600'}
        }
        solution_dict = {
            'pH_min': 5.5,
            'pH_max': 7.5,
            'ec_min': 0.0,
            'ec_max': 1.0,
            'solution_temp_min': 13,
            'solution_temp_max': 23,
        }
        power_dict = {
            'v_bat_min': 7.5,
            'v_bat_max': 14.5,
            'v_ps_min': 10.5,
            'v_ps_max': 14.5,
            'brd_temp_min': 0,
            'brd_temp_max': 50,
            'high_voltage': 5,
        }
        air_dict = {
            'rh_min': 0,
            'rh_max': 100,
            'pressure_min': 80_000,
            'pressure_max': 120_000,
            'air_temp_min': 17,
            'air_temp_max': 34,
        }
        light_dict = {
            'full_time': False,
            # seed
            'seed_days': 7,
            # vega
            'veg_morning_on': '5:00',
            'veg_morning_off': '18:00',
            'veg_main_on': '7:00',
            'veg_main_off': '21:00',
            'veg_evening_on': '9:00',
            'veg_evening_off': '23:00',
            'veg_uva_mins': 0,
            'veg_days': 66,
            # bloom
            'blm_morning_on': '7:00',
            'blm_morning_off': '17:00',
            'blm_main_on': '9:00',
            'blm_main_off': '19:00',
            'blm_evening_on': '11:00',
            'blm_evening_off': '21:00',
            'blm_uva_mins': 3,
            'blm_days': 33,
            # fruit
            'frt_morning_on': '7:00',
            'frt_morning_off': '17:00',
            'frt_main_on': '9:00',
            'frt_main_off': '19:00',
            'frt_evening_on': '11:00',
            'frt_evening_off': '21:00',
            'frt_uva_mins': 5,
            'frt_days': 22,
        }
        onewire_dict = {
            'miska': None,
            'air': None,
            'space': None,
        }
        anal_dict = {
            'pH_k': 0.0,
            'pH_b': 0.0,
            'ec_k': 0.0,
            'ec_b': 0.0,
        }
        sensors_dict = {
            'solution_temp': 'checked',
            'air_temp': 'checked',
            'space_temp': 'checked',
            'dht11': 'checked',
            'bmp085': '',
            'co2': '',
            'v_bat': 'checked',
        }
        return Settings(wifi_dict,
                        solution_dict,
                        air_dict,
                        power_dict,
                        light_dict,
                        onewire_dict,
                        anal_dict,
                        sensors_dict,
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
