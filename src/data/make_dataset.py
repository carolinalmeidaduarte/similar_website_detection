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
import os
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
    #options.add_argument('--headless')
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
                    level=logging.INFO,
                    format=log_fmt)


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
    #pd.DataFrame(outputs).to_csv(config["processed_data"])
    print(outputs)

"""


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    driver = webdriver.Chrome(
        options=options,
        executable_path="/usr/bin/chromedriver"
    )
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(DRIVER_WAIT_TIMEOUT)

    return driver

def get_tag_count(domain, html):

    soup = BeautifulSoup(html, "html.parser")
    tags = [tag.name for tag in soup.find_all() if tag.name in TAGS_IN_SCOPE]
    tags = dict(Counter(tags))
    tags['domain'] = domain

    return tags

def worker(domain_queue, return_list):
    driver = get_driver()

    while True:
        # exit if queue is empty
        if (domain_queue.empty()):
            logger.info("- shutting down driver and worker")
            driver.close()
            driver.quit()
            break

        enumerated_domain = domain_queue.get()
        queue_size = domain_queue.qsize()
        number = enumerated_domain[0]
        domain = enumerated_domain[1]

        # TODO: add a progress bar
        # sys.stdout.write("\r" + str(number) + "-" + domain)
        # sys.stdout.flush()
        logger.info(
            "\r" + str(number) + " processed | " +  str(queue_size)
            + " left. --> " + domain
        )

        try:
            driver.get("http://" + domain)
            time.sleep(5)
            html = driver.page_source.encode('utf-8')
            return_list.append(get_tag_count(domain, html))
        except Exception:
            logger.error("-failed to get data for {}".format(domain))
            # append none
            return_list.append(
                {
                    'div': None, 'a': None, 'img': None,
                    'span': None, 'ul': None, 'li': None,
                    'domain': domain
                }
            )

def scrape_domains(domains, cores=1):

    manager = multiprocessing.Manager()
    return_list = manager.list()

    # populate queue
    domains = [(i, domain) for i, domain in enumerate(domains)]
    domain_queue = multiprocessing.Queue()
    [domain_queue.put(i) for i in domains]

    jobs = []
    for i in range(cores - 1):
        p = multiprocessing.Process(target=worker, args=(domain_queue, return_list))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    return pd.DataFrame(return_list[:]).fillna(0.0)

if __name__ == '__main__':

    start_time = datetime.datetime.now()

    # get list of domains to scrape
    new_domains = bq_to_df(NEW_DOMAINS_QUERY)["domain"].to_list()

    logger.info("Processing {} domains.".format(len(new_domains)))

    # split the data in batchs of n size so that if the process fails at least a batch is processed
    new_domains_batches = (
        lambda new_domains, DOMAIN_BATCH_SIZE: [
            new_domains[i:i+DOMAIN_BATCH_SIZE]
            for i in range(0, len(new_domains), DOMAIN_BATCH_SIZE)
        ]
    )
    new_domains_batches = new_domains_batches(new_domains, DOMAIN_BATCH_SIZE)
    logger.info('The domains are split in {} batches.'.format(len(new_domains_batches)))

    for i, domain_batch in enumerate(new_domains_batches):
        logger.info("Processing batch number: {}".format(i))
        # lauch multiprocessing tasks to retrieve site data
        core_count = multiprocessing.cpu_count() - 1
        # core_count = 2
        domain_html_counts = scrape_domains(domain_batch, core_count)
        # Add timestamp
        domain_html_counts['timestamp'] = start_time
        # upload data to bq
        if len(domain_html_counts) > 0:
            df_to_bq(domain_html_counts, BQ_DOMAIN_HTML_TABLE)

    # log execution time
    end_time = datetime.datetime.now()
    logger.info((end_time - start_time).total_seconds())
    
"""