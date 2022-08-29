import yaml
import logging


# folder to load config file
CONFIG_FILE = "configuration.yaml"

# load yaml configuration file
def get_config_parameter(parameter):
    with open(CONFIG_FILE) as file:
        config = yaml.safe_load(file)

    return config[parameter]

def get_logger(source_function, log_name):
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=get_config_parameter(log_name),
                        format=log_fmt, level=logging.INFO)

    return logging.getLogger(source_function)