import configparser

def get_program_version():
    config = configparser.ConfigParser()
    config.read('./setup.cfg')
    return config['metadata']['version']
