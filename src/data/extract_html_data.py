# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from google.cloud import storage
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from src.utils.utils import *

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


def save_html_to_file(html, domain):
    bucket = get_storage_bucket()
    blob = bucket.blob(domain + ".html")
    try:
        response = blob.upload_from_string(html)
    except Exception as e:
        response = "failed to save file to gcs"

    return response


def process_html(domain):
    logger = get_logger(__name__, "log_data")

    # get html data from domain
    driver = get_driver()

    try:
        driver.get("http://" + domain)
        time.sleep(5)
        html = driver.page_source.encode('utf-8')
        save_html_to_file(html, domain)
        tags = get_tags(html, domain)
    except Exception:
        logger.error("-failed to get data for {}".format(domain))
        tags = {
                    'div': None, 'a': None, 'img': None,
                    'span': None, 'ul': None, 'li': None,
                    'domain': domain
                }

    return tags


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    logger = get_logger(__name__, "log_data")

    # get list of domains to scrape from raw data
    domains = pd.read_csv(get_path_to_file(get_config_parameter("target_domains")), index_col=False)["domain"]

    logger.info("Processing {} domains.".format(len(domains)))

    # lauch multiprocess to scrape domains in parallel
    pool = Pool(processes=get_config_parameter("multiprocess_tasks"))

    # collect outputs
    outputs = pool.map(process_html, domains)
    pool.close()
    pool.join()

    # write to output file
    pd.DataFrame(outputs).to_csv(get_path_to_file(get_config_parameter("raw_data")))
