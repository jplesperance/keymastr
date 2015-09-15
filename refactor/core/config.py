import os

import yaml


class UnknownSetting(Exception):
    def __init__(self, message):
        super(UnknownSetting, self).__init__(message)


class SettingsNamespace(object):
    def __getattr__(self, cls, attr):
        raise UnknownSetting(attr)


class PostloadHooks(object):
    @staticmethod
    def update_ssh_home(value):
        return os.path.expanduser(value)


def load_yaml(path, into='settings'):
    with open(path) as config_file:
        settings_object = globals()[into]

        for key, value in yaml.load(config_file.read()).items():
            if hasattr(PostloadHooks, 'update_' + key):
                value = getattr(PostloadHooks, 'update_' + key)(value)
            setattr(settings_object, key, value)


if __name__ != '__main__':
    settings = SettingsNamespace()



