# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import logging
import yaml

# folder to load config file
CONFIG_FILE = "configuration.yaml"

# load yaml configuration file
def get_config_parameter(parameter):
    with open(CONFIG_FILE) as file:
        config = yaml.safe_load(file)

    return config[parameter]


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

    try:
        driver = webdriver.Chrome(
            options=options,
            executable_path=get_config_parameter("chromedriver_path")
        )
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.implicitly_wait(get_config_parameter("driver_wait_timeout"))

    return driver

def get_tags(html, domain):
    soup = BeautifulSoup(html, "html.parser")
    tags_in_scope = ['div', 'ul', 'li', 'a', 'img', 'span']
    tags = [tag.name for tag in soup.find_all() if tag.name in tags_in_scope]
    tags = dict(Counter(tags))
    tags['domain'] = domain

    return tags

def process_html(domain):
    logger = logging.getLogger(__name__)

    # get html data from domain
    driver = get_driver()

    try:
        driver.get("http://" + domain)
        time.sleep(5)
        html = driver.page_source.encode('utf-8')
        tags = get_tags(html, domain)
    except Exception:
        logger.error("-failed to get data for {}".format(domain))
        tags = {
                    'div': None, 'a': None, 'img': None,
                    'span': None, 'ul': None, 'li': None,
                    'domain': domain
                }

    return tags



log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=get_config_parameter("log_data"),
                    format=log_fmt, level=logging.INFO)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    logger = logging.getLogger(__name__)

    # get list of domains to scrape from raw data
    domains = pd.read_csv("/Users/carolinaduarte/Documents/personal_projects/similar_website_detection/data/raw/raw_domain_list.csv", index_col=False)["domain"]

    logger.info("Processing {} domains.".format(len(domains)))

    # lauch multiprocess to scrape domains in parallel
    pool = Pool(processes=get_config_parameter("multiprocess_tasks"))

    # collect outputs
    outputs = pool.map(process_html, domains)
    pool.close()
    pool.join()

    # write to output file
    pd.DataFrame(outputs).to_csv(get_config_parameter("processed_data"))