import simplejson as json

CONFIG_NAME = 'configs/config.json'
LOCAL_NAME = 'configs/local.config.json'


class Config(object):
    def __init__(self, json_config):
        for key, value in json_config.items():
            setattr(self, key, value)
            # if isinstance(value, (list, tuple)):
            #     setattr(self, key, [Config(x) if isinstance(x, dict) else x for x in value])
            # else:
            #     setattr(self, key, Config(value) if isinstance(value, dict) else value)


class ConfigLoader:

    def __load_config(self, file_name):
        with open(file_name) as f:
            config = json.load(f, encoding='utf-8')
        return config

    def get_config(self):
        try:
            cfg = self.__load_config(CONFIG_NAME)
        except FileNotFoundError as e:
            raise RuntimeError(f'Cannot launch server without config: {e}')
        else:
            try:
                local_cfg = self.__load_config(LOCAL_NAME)
            except FileNotFoundError:
                local_cfg = None

            if local_cfg:
                cfg.update(local_cfg)
            return Config(cfg)


config = ConfigLoader().get_config()
