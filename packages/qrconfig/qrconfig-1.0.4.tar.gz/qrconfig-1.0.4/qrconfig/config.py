from collections import OrderedDict
from abc import abstractmethod

import confuse


class QRConfig:
    """abstract class for config"""

    @abstractmethod
    def read_config(self, *args):
        """read config and make fields available either as 'get' methods or as object's properties"""

    @abstractmethod
    def get(self, key: str):
        """return value of key. if value is a hierarchy itself, IQRConfig object is returned"""

    @abstractmethod
    def __getitem__(self, key: str):
        """return value of key. if value is a hierarchy itself, IQRConfig object is returned"""


class QRYamlConfig(QRConfig):
    def __init__(self, config_name=None):
        self.data = dict()

        if config_name is not None:
            self.read_config(config_name)

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value
        self.__dict__[key] = value

    def get(self, key):
        return self.data.get(key)

    def read_config(self, config_name='config.yaml'):
        config = confuse.Configuration('app', read=False)
        config.set_file(config_name)

        for x in config:
            d = config[x].get()
            self.data[x] = self.__parse_dict(d)
            self.__dict__[x] = self.data[x]

    def __parse_dict(self, d):
        if not isinstance(d, OrderedDict):
            return d

        obj = QRYamlConfig()
        for k, v in d.items():
            obj.data[k] = self.__parse_dict(v)
            obj.__dict__[k] = obj.data[k]
        return obj
