import configparser as cp


config = cp.ConfigParser()
# Loading the config file
def init():
    global config
    config.read('mytube.ini')
    print(f'config_parser::init config sections: {config.sections()}')


# Getting the config object
def getConfig(key_name):
    if len(config.sections()) == 0:
        init()
    print(config['APP_CONFIG'][key_name])
    return config['APP_CONFIG'][key_name]


if __name__ == "__main__":
    init()
    print( config.sections())

    print(getConfig('S3_BUCKET_NAME'))
    print(config['APP_CONFIG']['S3_BUCKET_NAME'])