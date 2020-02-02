import time
from random import randint

import pandas as pd
import requests
import logging
import sys

from datagen.datagen import ApiCallSheet
from datasource import datasource

from outputs import outputhelper

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(filename)s:%(lineno)d %(levelname)s - \n%(message)s')
log = logging.getLogger(__name__)

_ticketcount: str = ApiCallSheet.attr_names()[0]
_url: str = ApiCallSheet.attr_names()[1]
_duration: str = ApiCallSheet.attr_names()[2]


def run_bulk_queries(inputfile="input-raw-calls.csv", outputfile="results-timed-api"):
    csv_path = datasource.get_file_path(inputfile)

    urls_to_call = pd.read_csv(csv_path, header=0, names=[_ticketcount, _url],
                               usecols=[_ticketcount, _url])

    results = []
    for index, row in urls_to_call.iterrows():
        ms = time_api(row, index)
        results.append(ms)

    log.info(f"{len(results)} results gathered")

    urls_to_call[_duration] = pd.Series(results)
    log.debug(urls_to_call)

    outputhelper.save_to_input_directory(urls_to_call, outputfile)


def time_api(row, index):
    url = row[_url]

    start = time.perf_counter()
    # this is a subsitute for actually calling
    time.sleep(randint(1, 300) / 1000)  # fake a sleep for 1-n ms
    # response = requests.get(url)
    duration = time.perf_counter() - start

    elapsed_ms = int(duration * 1000)

    response = True  # this is removed for real calls
    if not response:
        raise Exception(f'API call to: {url} failed. Response was {response}')
    else:
        log.info(f"index: {index},  elapsed time {elapsed_ms} ms, url: {url}")
        return elapsed_ms


if __name__ == '__main__':
    # run_bulk_queries()
    run_bulk_queries(outputfile="llalala")
