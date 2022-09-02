import yaml
import logging
import os
from google.cloud import storage

# folder to load config file
CONFIG_FILE = "configuration.yaml"

def get_main_path():
    main_path = os.environ['PYTHONPATH'].split(os.pathsep)[0]
    return main_path

def get_path_to_file(file_name):
    path_to_file = get_main_path() + "/" + file_name
    return path_to_file

# load yaml configuration file
def get_config_parameter(parameter):
    with open(get_path_to_file(CONFIG_FILE)) as file:
        config = yaml.safe_load(file)

    return config[parameter]

def get_logger(source_function, log_name):
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=get_path_to_file(get_config_parameter(log_name)),
                        format=log_fmt, level=logging.INFO)

    return logging.getLogger(source_function)

def get_storage_bucket():
    storage_client = storage.Client()
    bucket = storage_client.bucket(get_config_parameter("google_cloud_storage_bucket"))
    return bucket
