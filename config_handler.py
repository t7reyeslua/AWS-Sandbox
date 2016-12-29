import configparser

config = configparser.ConfigParser()
config_file = config.read('aws.config.local')
if config_file == []:
    config_file = config.read('aws.config')