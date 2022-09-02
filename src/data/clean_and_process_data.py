import pandas as pd
import datetime
from src.utils.utils import *

if __name__ == '__main__':
    start_time = datetime.datetime.now()

    logger = get_logger(__name__, "log_data")

    raw_data = pd.read_csv(get_path_to_file(get_config_parameter("raw_data")), index_col=False)
    clean_data = raw_data.drop_duplicates()

    clean_data.to_csv(get_path_to_file(get_config_parameter("processed_data")))

