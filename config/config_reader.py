import configparser

def read_config(filepath='config/config.ini'):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config