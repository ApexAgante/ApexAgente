from os import path, remove


def check_config():
    if path.isfile('config.json'):
        remove('config.json')
