import os


def environs_set_default():
    dictionary = {
        'DJANGO_SETTINGS_MODULE': 'application.settings',
    }
    for k, v in dictionary.items():
        os.environ.setdefault(k, v)
